from schemas.base import BaseModel
from schemas.image import ImageSchema


class GroupSchema(BaseModel):
    name: str


class GroupWithImagesSchema(GroupSchema):
    """
    Provides correct openapi schema rendering
    """
    count: int
    images: list[ImageSchema]
