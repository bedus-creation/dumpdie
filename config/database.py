# this is just for testing purposes
from masoniteorm.connections import ConnectionResolver

DATABASES = {"default": "sqlite", "sqlite": {"driver": "sqlite", "database": ":memory:"}}

DB = ConnectionResolver().set_connection_details(DATABASES)
