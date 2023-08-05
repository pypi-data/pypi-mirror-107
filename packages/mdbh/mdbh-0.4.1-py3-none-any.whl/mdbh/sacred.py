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
import pickle
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import pandas as pd
from pymongo.database import Collection
from pymongo.database import Database

from mdbh import caching
from mdbh import data
from mdbh.core import _wrap_ids
from mdbh.data import _get_gridfs_data


def _get_dataframe_query(db: Database,
                         query: dict,
                         collection: Union[str, Collection]) -> pd.DataFrame:
    """Get a DataFrame from a MongoDB query.

    Args:
        db: Database instance to query.

        query: The query.

        collection: Collection to query.

    Returns:
        DataFrame of query result.
    """
    if type(db) != Database:
        raise TypeError("db needs to be a PyMongo Database instance. "
                        "Use mdbh.get_mongodb")
    # Query database and convert to DataFrame
    res = db[collection].find(query)
    df = pd.DataFrame(list(res))

    return df


def _get_run_ids(db: Database) -> List[int]:
    """Get all run IDs of a database.

    Args:
        db: Database instance to query.

    Returns:
        List of run IDs of the database.
    """
    return _get_dataframe_query(db, {}, "runs")['_id'].tolist()


def _get_dataframe(db: Database,
                   ids: Optional[Union[int, List[int], Tuple[int, ...]]] = None,
                   include_artifacts: bool = False) -> pd.DataFrame:
    """Get all experiments from a Sacred Database in a DataFrame.
    Metrics and configurations are concatenated into a single DataFrame for
    convenience.

    Args:
        db: Database instance to query.

        ids: Optional run ID or list of IDs to get.
             If None, all IDs are queried.

        include_artifacts: Whether to include a column for artifacts.
                           Artifacts can then be resolved via
                           :func:resolve_artifacts().

    Returns:
        DataFrame of the corresponding Database.
    """
    # Wrap ids into list
    ids = _wrap_ids(ids) if ids is not None else ids

    # Get all metric and run logs
    query = {} if ids is None else {"run_id": {"$in": ids}}
    df_metric = _get_dataframe_query(db, query, "metrics")

    query = {} if ids is None else {"_id": {"$in": ids}}
    df_runs = _get_dataframe_query(db, query, "runs")
    df_runs.index = df_runs['_id'].tolist()

    # Extract config dict into columns
    tmp = pd.DataFrame(df_runs['config'].tolist())
    tmp = tmp.rename(lambda x: f"config.{x}", axis=1)
    tmp.index = df_runs.index
    df_runs = pd.concat([df_runs, tmp], axis=1)

    # Extract experiment dict into columns
    tmp = pd.DataFrame(df_runs['experiment'].tolist())
    tmp = tmp.rename(lambda x: f"experiment.{x}", axis=1)
    tmp.index = df_runs.index
    df_runs = pd.concat([df_runs, tmp], axis=1)

    # Clean up DataFrame
    df_m_del_cols = ['_id', ]
    df_r_del_cols = ['experiment', 'format', 'command', 'start_time', 'meta',
                     'resources', 'info', 'heartbeat',
                     'result', 'stop_time', 'fail_trace', 'captured_out',
                     'omniboard']

    if not include_artifacts:
        df_r_del_cols += ['artifacts']

    for i in df_r_del_cols:
        if i in df_runs.columns.tolist():
            del df_runs[i]

    # When there are no recorded metrics, just return runs dataframe
    if len(df_metric) == 0:
        return df_runs.rename(columns={'_id': 'id'})

    # Set run_id (metrics), _id (runs) as index of DataFrames for later join
    df_metric.index = df_metric['run_id'].tolist()

    # Get all IDs
    id_list = df_runs['_id'].unique().tolist()

    # Get metric column names
    metrics = df_metric['name'].unique().tolist()
    cols = [f"metrics.{i}" for i in metrics]

    # Create new DatFrame with extracted metrics
    df_metrics_full = pd.DataFrame(columns=["_id", *cols])
    for id in id_list:
        df_metrics_full = df_metrics_full.append(pd.DataFrame([[id]], columns=['_id']))
        df_metrics_full.index = df_metrics_full['_id'].tolist()
        for col in metrics:
            try:
                df_metrics_full[f'metrics.{col}'][id] = df_metric[(df_metric["run_id"] == id) & (df_metric["name"] == col)]['values'].values[0]
            except IndexError:
                df_metrics_full[f'metrics.{col}'][id] = float("NaN")
            # Extract float values for test metrics
            try:
                if "test_" in col and len(tmp_vals := df_metrics_full[f'metrics.{col}'][id]) == 1:
                        df_metrics_full[f'metrics.{col}'][id] = tmp_vals[0]
            except TypeError or IndexError:
                pass

    for i in df_m_del_cols:
        if i in df_metrics_full.columns.tolist():
            del df_metrics_full[i]

    df = df_runs.join(df_metrics_full)
    df = df.rename(columns={'_id': 'id'})

    return df.infer_objects()


def _get_dataframe_cached(db: Database,
                          ids: Optional[Union[int, List[int], Tuple[int, ...]]] = None,
                          include_artifacts: bool = False,
                          verify: bool = False,
                          force: bool = False) -> pd.DataFrame:
    """Retrieve DataFrame from MongoDB and cache result locally.

    Caution: When retrieving the full database (using `ids = None`), by default
    it is not verified that the local version is up-to-date with the remote
    version. To verify and possibly re-download the up-to-date database,
    use `verify=True`.

    Args:
        db: Database instance to query.

        ids: Optional run ID or list of IDs to get.
             If None, all IDs are queried.

        include_artifacts: Whether to include a column for artifacts.
                           Artifacts can then be resolved via
                           :func:resolve_artifacts().

        verify: Whether to verify that local version is up-to-date with remote
                database. Only used when `ids=None`.

        force: Whether to force re-loading from MongoDB even if cached
               version is available.

    Returns:
        DataFrame of the corresponding Database.
    """

    filename = f"{db.name}_ids_{ids}_artifacts_{include_artifacts}.pickle"
    get_data = lambda: pickle.dumps(_get_dataframe(db, ids, include_artifacts), protocol=4)
    path = caching.get(filename, get_data, force)

    df_local = pd.read_pickle(path)

    if ids is None and verify and not force:
        print("Verifying local version.")
        ids_local = df_local['id'].tolist()
        ids_remote = _get_run_ids(db)
        if ids_local != ids_remote:
            print("Remote version has been altered. Re-downloading.")
            path = caching.get(filename, get_data, force=True)
            df_local = pd.read_pickle(path)

    return df_local


def get_dataframe(db: Database,
                  ids: Optional[Union[int, List[int], Tuple[int, ...]]] = None,
                  include_artifacts: bool = False,
                  cache: bool = False,
                  **kwargs):
    """Get all experiments from a Sacred Database in a DataFrame.
    Metrics and configurations are concatenated into a single DataFrame for
    convenience.

    Args:
        db: Database instance to query.

        ids: Optional run ID or list of IDs to get. If None, all IDs are queried.

        include_artifacts: Whether to include a column for artifacts.
                           Artifacts can then be resolved via
                           :func:resolve_artifacts().

        cache: Whether to cache the downloaded DataFrame. This can be useful
               when retrieving very large databases. See :func:`_get_dataframe_cached()`
               for details and keyword arguments.

        **kwargs: See :func:`_get_dataframe_cached()`.

    Returns:
        DataFrame of the corresponding Database.
    """
    if cache:
        return _get_dataframe_cached(db, ids, include_artifacts, **kwargs)
    else:
        return _get_dataframe(db, ids, include_artifacts)


def get_run_names(db: Database):
    """Get a DataFrame containing only the run ID experiment names.

    Args:
        db:

    Returns:
        DataFrame with run IDs and experiment names.
    """
    df_runs = _get_dataframe_query(db, {}, "runs")
    df_names = df_runs["experiment"].map(lambda x: x['name'])
    df_names.index = df_runs['_id'].tolist()
    return df_names


def resolve_artifacts(db: Database, df: pd.DataFrame) -> pd.DataFrame:
    """Maps the artifact column as retrieved from the database in
    get_df_full(..., return_artifacts=True) into a dictionary of the form
    {filename1: filecontent1, filename2:  filecontent2....}.

    Usage:

        df = mdbh.get_df_full(db, return_artifacts=True)
        df = mdbh.resolve_artifacts(db, df)

    Args:
        db: Database instance.
        df: The Dataframe with 'artifacts' column.

    Returns:
        The Dataframe with a transformed column
    """
    def map_artifacts(db: Database, x):
        return {artifact["name"]: _get_gridfs_data(db, artifact["file_id"]) for artifact in x}
    df["artifacts"] = df["artifacts"].map(lambda x: map_artifacts(db, x))
    return df


def get_artifact_names(db: Database, id: int) -> List[str]:
    """Get the names of the artifacts from a run ID.

    Args:
        db: Database instance.
        id: Run ID.

    Returns:
        List of names of the ID's artifacts.
    """
    df = get_dataframe(db, [id], include_artifacts=True)
    return [a['name'] for a in df.loc[id]['artifacts']]


def get_artifact(db: Database,
                 id: int,
                 name: str,
                 force: bool = False) -> Path:
    """Get path to artifact from a Database and run ID.
    The artifacts are downloaded and cached by default.

    Args:
        db: Database instance to query.

        id: Run ID to get artifact from.

        name: Name of artifact to get.
              To obtain a list of available names, use
              :func:`get_artifact_names()`

        force: Whether to force downloading of the artifact, even if cached
               version is available.

    Returns:
        Path to the downloaded or cached artifact.
    """
    def _get_data():
        """Download artifact from MongoDB."""
        df = get_dataframe(db, [id], include_artifacts=True)
        artifacts = [a for a in df.loc[id]['artifacts'] if a['name'] == name]
        if len(artifacts) == 0:
            raise ValueError(f"No artifact found with name {name} for run ID {id}.")
        if len(artifacts) > 1:
            raise ValueError(f"Found more than one artifact with name {name} for run ID {id}.")
        artifact = artifacts[0]
        print(f"Downloading artifact from MongoDB.")
        return _get_gridfs_data(db, artifact['file_id'])

    filename = f"{db.name}_{id}_{name}"
    return caching.get(filename, _get_data, force)


def add_artifact(db: Database,
                 id: int,
                 path: Union[str, Path],
                 name: Optional[str] = None):
    """Adds an artifact to an existing Sacred experiment with run ID.

    Args:
        db: Database instance to query.

        id: Run ID to add artifact to.

        path: System path to the file to add as an artifact.

        name: Optionally specify name of artifact.
              If None, name is used from specified `path`.
    """
    if id not in _get_run_ids(db):
        raise ValueError(f"ID {id} not found in database.")

    path = Path(path)
    name = name or path.name

    # Get artifacts already part of the experiment
    query = {"_id": {"$in": [id]}}
    res = db["runs"].find(query)
    artifacts = res[0]['artifacts']

    # Check if artifact name is available
    if name in [a['name'] for a in artifacts]:
        raise ValueError(f"Name {name} already used by another artifact.")

    # Add artifact to GridFS, use layout specified by Sacred
    db_filename = f"artifact://runs/{id}/{name}"
    object_id = data._put_gridfs_data(db,
                                      path,
                                      filename=db_filename,
                                      metadata=None,
                                      content_type=None)

    # Append to existing artifacts and update database entry
    artifacts.append(dict(name=name, file_id=object_id))
    db["runs"].update_one(query, {"$set": {"artifacts": artifacts}})

    return


def get_metric(db: Database, id: int, metric: str) -> dict:
    """Get metric from a Sacred experiment ID.

    Args:
        db: PyMongo Database instance.

        id: Run ID of experiment.

        metric: Name of the metric to get.

    Returns:
        dict, metric dictionary containing name, value, steps, etc.
    """
    if type(db) != Database:
        raise TypeError("db needs to be a PyMongo Database instance. "
                        "Use mdbh.get_mongodb")

    metrics = db.get_collection('metrics')
    return metrics.find_one({"run_id": id, "name": metric})
