from bson import ObjectId
from pydantic import BaseModel as _BaseModel
from pydantic import Field
from pydantic import validator


def validate_object_id(value: ObjectId | str) -> str:
    if not isinstance(value, (ObjectId, str)):
        raise TypeError("ObjectId is required")
    return str(value)


class BaseModel(_BaseModel):
    id: str = Field(alias="_id")  # noqa

    @validator("id", pre=True)
    def validate_object_id(cls, value: ObjectId | str) -> str:
        return validate_object_id(value)

    class Config:
        arbitrary_types_allowed = True
