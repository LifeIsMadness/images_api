from typing import Annotated, Optional

from fastapi import APIRouter
from fastapi import Query

from routers.dependencies import DatabaseAnnotated
from schemas.group import GroupWithImagesSchema
from schemas.image import StatusEnum
from services.group_service import GroupService

router = APIRouter(
    prefix="/api/v1/groups",
    tags=["groups"],
)


@router.get("/", response_model=list[GroupWithImagesSchema], response_model_by_alias=False)
def get_groups(
    db: DatabaseAnnotated,
    status: Annotated[Optional[StatusEnum], Query()] = None,
    page: Annotated[Optional[int], Query(gt=0)] = None,
    page_size: Annotated[Optional[int], Query(gt=0)] = None,
):
    service = GroupService(db)
    return service.get_groups_with_images(status, page, page_size)
