from typing import Optional

from pymongo import DESCENDING

from models.group import GroupDAO
from schemas.group import GroupWithImagesSchema
from services.base import BaseService


class GroupService(BaseService):
    def _paginate(self, page: int, page_size: int) -> list[dict]:
        return [{"$skip": (page - 1) * page_size}, {"$limit": page_size}]

    def get_groups_with_images(
        self, status: str | None, page: Optional[int] = None, page_size: Optional[int] = None
    ) -> list[GroupWithImagesSchema]:
        """
        Returns a list of groups with associated images.
        Uses mongo's aggregation pipelines.
        """
        pipeline = []
        if page and page_size:
            pipeline = self._paginate(page, page_size)
        pipeline.extend(
            [
                {
                    "$lookup": {
                        "from": "images",
                        "localField": "_id",
                        "foreignField": "groupId",
                        "pipeline": [
                            {
                                "$sort": {"createdAt": DESCENDING},
                            },
                        ],
                        "as": "images",
                    },
                },
                {
                    "$set": {
                        "count": {"$size": "$images"},
                    }
                },
            ]
        )
        if status:
            pipeline[-2]["$lookup"]["pipeline"].insert(0, {"$match": {"status": status}})  # noqa

        groups = GroupDAO(self.db).aggregate(pipeline=pipeline)
        return [GroupWithImagesSchema(**g) for g in groups]
