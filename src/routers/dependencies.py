from typing import Annotated

from fastapi import Depends
from pymongo.database import Database

from config.database import get_db

DatabaseAnnotated = Annotated[Database, Depends(get_db)]
