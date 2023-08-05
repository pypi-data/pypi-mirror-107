# -*- coding: utf-8 -*-

import os

from pathlib import Path
from py4web.core import required_folder
HOME = str(Path.home())

# db settings
APP_FOLDER = HOME

# DB_FOLDER:    Sets the place where migration files will be created
#               and is the store location for SQLite databases
DB_FOLDER = os.path.join(APP_FOLDER, "databases")
DB_URI = "sqlite://vtile_cache.db"
# DB_POOL_SIZE = 1
DB_MIGRATE = True
# DB_FAKE_MIGRATE = False  # maybe?

# location where to store uploaded files:
UPLOAD_FOLDER = required_folder(APP_FOLDER, "uploads")

# location where static files are stored:
STATIC_FOLDER = os.path.join(APP_FOLDER, "static")
STATIC_UPLOAD_FOLDER = required_folder(STATIC_FOLDER, "uploads")

# logger settings
LOGGERS = [
    "info:stdout"
]  # syntax "severity:filename" filename can be stderr or stdout

# Default value for cache expiration threashold
CACHE_EXPIRE = float('Inf')

CACHE_NEW = False

CACHE_ON_CLIENT = False

# try import private settings
try:
    from .settings_private import *
except (ImportError, ModuleNotFoundError):
    pass
