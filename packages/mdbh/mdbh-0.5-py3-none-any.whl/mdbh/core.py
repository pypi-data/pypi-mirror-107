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

import configparser
from pathlib import Path
from typing import List
from typing import Tuple
from typing import Union

from pymongo import MongoClient
from pymongo.database import Database


def get_uri(conf_path: Union[Path, str],
            db_name: str) -> str:
    """Creates MongoDB connection URI from configuration file
    and database name.

    Args:
        conf_path: Path to the .mongo.conf configuration file.

        db_name: Name of the database to connect to.

    Returns:
        uri, MongoDB connection URI.
    """
    # Get path
    p = Path(conf_path).expanduser().absolute()

    if not p.exists():
        raise ValueError(f"Path {p} doest not exist.")

    # Load MongoDB configuration
    config = configparser.ConfigParser()
    config.read(p)

    server = config['SERVER']['ip']
    port = config['SERVER']['port']

    if 'username' in config['USER'].keys() and 'password' in config['USER'].keys():
        user = config['USER']['username']
        pw = config['USER']['password']

        if "auth" in config['USER'].keys():
            auth = config['USER']['auth']
        else:
            auth = "SCRAM-SHA-1"

        if "auth_db" in config['USER'].keys():
            auth_db = config['USER']['auth_db']
        else:
            auth_db = "admin"

        uri = f"mongodb://{user}:{pw}@{server}:{port}/{db_name}?authSource={auth_db}&authMechanism={auth}"

    else:
        print("No username and password specified.")
        uri = f"mongodb://{server}:{port}/{db_name}"

    return uri


def get_conf_databases(conf_path: Union[Path, str]) -> List[str]:
    """Get the name of databases specified in .mongo.conf config file.
    If none specified, uses "sacred" as default.

    Args:
        conf_path: Path to the .mongo.conf configuration file.

    Returns:
        List of Sacred databases.

    """
    # Get path
    p = Path(conf_path).expanduser().absolute()

    if not p.exists():
        raise ValueError(f"Path {p} doest not exist.")

    # Load MongoDB configuration
    config = configparser.ConfigParser()
    config.read(p)

    if 'DATABASES' not in config.keys():
        return ["sacred"]

    return [db for db in config['DATABASES'].values()]


def get_client(conf_path: Union[Path, str],
               db_name: str = "sacred") -> MongoClient:
    """Get a MongoClient using the specified configuration."""

    uri = get_uri(conf_path, db_name)
    return MongoClient(uri)


def get_mongodb(conf_path: Union[Path, str],
                db_name: str = "sacred") -> Database:
    """Get a MongoDB Database instance.

    Args:
        conf_path: Path to MongoDB configuration file.

        db_name: Name of the database.

    Returns:
        A PyMongo Database instance.

    """
    client = get_client(conf_path, db_name)
    db = client.get_database()

    if not ('metrics' in db.collection_names() and 'runs' in db.collection_names()):
        print("WARNING: No 'metrics' or 'runs' collection found in database. "
              "Are you sure this is a Sacred database? "
              "If this is intended, you can safely ignore this message.")

    return db


def _wrap_ids(ids: Union[int, List[int], Tuple[int, ...]]) -> List[int]:
    """Wrap input ids into list of ints.

    Args:
        ids: Single or multiple ids.

    Returns:
        List of ids.
    """
    return list(ids) if isinstance(ids, (tuple, list, set)) else [ids]
