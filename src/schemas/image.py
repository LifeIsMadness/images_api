from datetime import datetime
from enum import Enum
from typing import Optional, Union

from bson import ObjectId

from pydantic import Field, validator

from schemas.base import BaseModel, validate_object_id


class StatusEnum(str, Enum):
    NEW = "new"
    ACCEPTED = "accepted"
    REVIEW = "review"
    DELETED = "deleted"


class ImageSchema(BaseModel):
    """
    Provides correct openapi schema rendering
    """
    url: str
    created_at: datetime = Field(alias="createdAt")
    status: StatusEnum
    group_id: str = Field(alias="groupId")

    @validator("group_id", pre=True)
    def validate_object_id(cls, value: ObjectId | str) -> str:
        return validate_object_id(value)


class ImageUpdateSchema(BaseModel):
    id: Union[str, None] = Field(default=None, description="Read only field")
    status: Union[StatusEnum, None] = Field(default=None, description="Write only field")

