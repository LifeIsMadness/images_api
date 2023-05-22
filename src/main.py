from fastapi import FastAPI
from mangum import Mangum

import routers

app = FastAPI(title="ImagesAPI")
app.include_router(router=routers.images_router)
app.include_router(router=routers.groups_router)

# you can use this handler for aws lambda (main.handler)
handler = Mangum(app)
