from bson import ObjectId

from models.base import DAOBase


class ImageDAO(DAOBase):
    """
    Performs all image db entity manipulations
    """

    DATA_COLLECTION_NAME = "images"

    def update_image(self, image_id: str, **kwargs) -> bool:
        """
        Returns True if update operation was successfull(even if same values)
        """
        query = {"_id": ObjectId(image_id)}, {"$set": kwargs}
        result = self.db[self.DATA_COLLECTION_NAME].update_one(*query)

        return result.matched_count > 0
