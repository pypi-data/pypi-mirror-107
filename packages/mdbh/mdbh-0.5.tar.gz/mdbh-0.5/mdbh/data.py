# -*- coding: utf-8 -*-1.3
# Copyright (C) 2020  The MDBH Authors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from pathlib import Path

from datetime import datetime

from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import gridfs
from bson.objectid import ObjectId

from pymongo.database import Collection
from pymongo.database import Database
from pymongo.results import DeleteResult

from mdbh import caching
from mdbh.environ import get_data_collection


def _delete_gridfs_data(db: Database,
                        id: Union[str, ObjectId]):
    """Delete GridFS object.

    Args:
        db: MongoDB Database instance.

        id: ObjectID of the GridFS data entry.
    """
    id = id if isinstance(id, ObjectId) else ObjectId(id)
    fs = gridfs.GridFS(db)
    fs.delete(id)
    return


def _get_gridfs_data(db: Database,
                     id: Union[str, ObjectId]) -> bytes:
    """Retrieves file content from GridFS by ObjectID.
    E.g., this corresponds to the way Sacred saves artifacts.

    Args:
        db: Database instance to query.

        id: Object id of the GridFS data entry.

    Returns:
        The binary file content.
    """
    id = id if isinstance(id, ObjectId) else ObjectId(id)
    gr = gridfs.GridFS(db)
    return gr.get(id).read()


def _put_gridfs_data(db: Database,
                     path: Union[str, Path],
                     **kwargs) -> ObjectId:
    """Put binary data into GridFS.

    Args:
        db: MongoDB Database instance.

        path: System path to the file

        **kwargs: Passed to GridFS.put()

    Returns:
        ObjectID of the created GridFS entry.
    """
    with open(path, 'br') as fh:
        # Add file to GridFS
        fs = gridfs.GridFS(db)
        new_data_id = fs.put(fh, **kwargs)

    return new_data_id


def _get_data_collection_entry(db: Database,
                               id: Union[str, ObjectId]) -> Tuple[Collection, dict]:
    """Get entry and collection from binary data collection.

    Args:
        db: MongoDB Database instance.

        id: ObjectID of the entry.

    Returns:
        collection, entry
    """
    id = id if isinstance(id, ObjectId) else ObjectId(id)
    collection = db[get_data_collection()]
    entry = collection.find_one({"_id": id})
    return collection, entry


def delete_data(db: Database,
                id: Union[str, ObjectId]) -> DeleteResult:
    """Delete data and object entry.
    To delete all data, use
    `[delete_data(db, id) for id in [d['_id'] for d in list_data(db)]]`

    Args:
        db: MongoDB Database instance.
        id: ObjectId of the object to delete.

    Returns:
        DeleteResult
    """
    id = id if isinstance(id, ObjectId) else ObjectId(id)
    collection, entry = _get_data_collection_entry(db, id)

    if entry is not None:
        # Delete corresponding binary data
        data_id = entry["data_id"]
        _delete_gridfs_data(db, data_id)
    else:
        print(f"No object with matching ID found.")

    # Delete entry
    return collection.delete_one({"_id": id})


def find_data(db: Database,
              query: Optional[dict] = None) -> List[dict]:
    """Find data in binary data collection.
    E.g., to query a specific object id, use `query = {'id'=ObjectId(...)}`.

    Args:
        db: MongoDB Database instance.

        query: MongoDB query.

    Returns:
        List of retrieved documents matching the query.
    """

    query = query or {}
    if "id" in query.keys():
        query['_id'] = query.pop('id')

    return list(db[get_data_collection()].find(query))


def get_data(db: Database,
             id: Union[str, ObjectId],
             force: bool = False) -> Path:
    """Get path to artifact from a Database and object ID.
    The artifacts are downloaded and cached by default.

    Args:
        db: Database instance to query.

        id: Object ID to get binary data from.

        force: Whether to force downloading of the artifact, even if cached
               version is available.

    Returns:
        Path to the downloaded or cached artifact.
    """
    id = id if isinstance(id, ObjectId) else ObjectId(id)
    collection, entry = _get_data_collection_entry(db, id)
    filename = f"{db.name}_{get_data_collection()}_id_{id}_{entry['filename']}"
    data_id = entry['data_id']
    _get_data = lambda: _get_gridfs_data(db, data_id)

    return caching.get(filename, _get_data, force)


def list_data(db: Database) -> List[dict]:
    """List all binary data in data collection.

    Args:
        db: MongoDB Database instance.

    Returns:
        List of retrieved documents as dict.
    """
    return find_data(db, {})


def put_data(db: Database,
             path: Union[str, Path],
             name: Optional[str] = None,
             **kwargs) -> ObjectId:
    """Put binary data into a database.
    The collection name is determined by the MDBH_DATA_COLLECTION environment
    variable, see `mdbh.environ`.

    See Also:
        To read the data from the database with caching, see :func:`get_data`.
        To delete the data, see :func:`delete_data`.
        To find data, see :func:`find_data`.

    Args:
        db: MongoDB Database instance

        path: System path to file containing the data.

        name: Optional name for database entry.

        **kwargs: Optional metadata arguments to identify the file.

    Returns:
        ObjectId instance of the new database entry.
    """
    if isinstance(path, str):
        path = Path(path)

    # Upload data to GridFS database
    data_id = _put_gridfs_data(db, path)

    # Insert into collection
    res = db[get_data_collection()].insert_one(
        dict(filename=path.name, name=name, date=datetime.now().isoformat(),
             data_id=data_id, **kwargs))

    return res.inserted_id


def replace_data(db: Database,
                 id: Union[str, ObjectId],
                 path: Union[str, Path]):
    """Replace binary data associatet with entry id.

    Args:
        db: MongoDB Database instance.

        id: ObjectId of document.

        path: Path to new data file.
    """
    id = id if isinstance(id, ObjectId) else ObjectId(id)
    collection, entry = _get_data_collection_entry(db, id)

    if entry is not None:
        # Delete corresponding binary data
        data_id = entry["data_id"]
        _delete_gridfs_data(db, data_id)
    else:
        print(f"No object with matching ID found.")

    if isinstance(path, str):
        path = Path(path)

    # Upload new data to GridFS
    new_data_id = _put_gridfs_data(db, path)

    # Update/replace document
    entry['data_id'] = new_data_id
    entry['filename'] = path.name
    entry['date_modified'] = datetime.now().isoformat()
    collection.replace_one({"_id": id}, entry)
    return
