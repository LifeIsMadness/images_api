import os
from typing import TYPE_CHECKING

import pymongo

if TYPE_CHECKING:
    from pymongo.database import Database

client: pymongo.MongoClient = pymongo.MongoClient(os.getenv("MONGODB_URL"))


def get_db() -> "Database":
    return client.get_default_database(os.getenv("MONGODB_NAME", "master"))


class DBContext:
    def __init__(self, db: "Database"):
        self.db = db
