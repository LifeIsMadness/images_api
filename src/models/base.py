from config.database import DBContext


class DAOBase(DBContext):
    def aggregate(self, *, pipeline: list[dict[str, dict]]) -> list[dict]:
        return list(self.db[self.DATA_COLLECTION_NAME].aggregate(pipeline=pipeline))  # type: ignore[attr-defined]
