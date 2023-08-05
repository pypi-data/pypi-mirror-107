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

import os
from pathlib import Path

import configparser

# System-independent path for MDBH config file
CONFIG_PATH = Path("~/.config/mdbh/mdbh.conf").expanduser()


def get():
    """Get the MDBH environment variables and values."""
    return {k: val for k, val in os.environ.items() if k[:5] == "MDBH_"}


def create_config_file():
    """Create default configuration file."""
    from tempfile import gettempdir

    print(f"No MDBH config file found at {CONFIG_PATH}. Creating default.")
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    config = configparser.ConfigParser()
    config['ENVIRON'] = dict(cache_dir=gettempdir(),
                             data_collection="binarydata")

    with open(CONFIG_PATH, 'w') as configfile:
        config.write(configfile)


def set_defaults():
    """Set the default MDBH environment variables and values."""

    if not CONFIG_PATH.exists():
        create_config_file()

    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    # Read config file
    cache_dir = Path(config.get("ENVIRON", "cache_dir")).expanduser()
    set_cache_dir(str(cache_dir))

    data_collection = config.get("ENVIRON", "data_collection")
    set_data_collection(data_collection)


def get_cache_dir() -> str:
    """get the MDBH cache directory environment variable."""
    return os.environ['MDBH_CACHE_DIR']


def set_cache_dir(cache_dir: str):
    """Set the MDBH cache directory environment variable."""
    os.environ['MDBH_CACHE_DIR'] = cache_dir
    # Create directory and parents, if non-existent
    Path(cache_dir).mkdir(parents=True, exist_ok=True)


def get_data_collection() -> str:
    """get the MDBH data collection environment variable."""
    return os.environ['MDBH_DATA_COLLECTION']


def set_data_collection(data_collection: str):
    """get the MDBH data collection environment variable."""
    os.environ['MDBH_DATA_COLLECTION'] = data_collection
