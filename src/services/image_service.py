from datetime import datetime
from datetime import timedelta

from fastapi import HTTPException
from pymongo.database import Database
from starlette import status

from models.image import ImageDAO
from schemas.image import ImageUpdateSchema
from services.base import BaseService


class ImageUpdater(BaseService):
    def __init__(self, db: Database, _id: str, image: ImageUpdateSchema):
        super().__init__(db)
        self.id = _id
        self.image = image

    def __call__(self) -> ImageUpdateSchema:
        return self.update_image()

    def update_image(self) -> ImageUpdateSchema:
        is_updated = ImageDAO(self.db).update_image(self.id, **self.image.dict(exclude_none=True, by_alias=True))
        if not is_updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Image with ID {self.id} not found")
        return ImageUpdateSchema(**self.image.dict(exclude_none=True), id=self.id)


class ImageStats(BaseService):
    def get_image_stats_for_period(self, period=30) -> dict[str, int]:
        """
        Returns the number of images for each status for the period
        :param period: days
        """
        today = datetime.utcnow()
        before = (today - timedelta(days=period - 1)).replace(hour=0, minute=0, second=0, microsecond=0)
        pipeline = [
            {
                "$match": {
                    "createdAt": {"$lte": today, "$gte": before},
                },
            },
            {
                "$group": {
                    "_id": "$status",
                    "count": {"$count": {}},
                },
            },
            {
                "$project": {"_id": 0, "status": "$_id", "count": 1},
            },
        ]
        result = {}
        for dict_ in ImageDAO(self.db).aggregate(pipeline=pipeline):  # type: ignore[arg-type]
            result[dict_["status"]] = dict_["count"]

        return result
