from fastapi import APIRouter

from routers.dependencies import DatabaseAnnotated
from schemas.image import ImageUpdateSchema
from services.image_service import ImageUpdater, ImageStats

router = APIRouter(
    prefix="/images",
    tags=["images"],
)


@router.get("/stats")
def get_image_stats(db: DatabaseAnnotated):
    return ImageStats(db).get_image_stats_for_period()


@router.patch("/{image_id}", response_model=ImageUpdateSchema)
def update_image(image_id: str, image: ImageUpdateSchema, db: DatabaseAnnotated):
    updated_image = ImageUpdater(db, image_id, image)()
    return updated_image
