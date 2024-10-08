"""
Stars Portal API 
This is backend for Stars Portal application
"""

from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import RedirectResponse
from loguru import logger
from .utils import generate_pydantic_models, generate_crud_routers
from .db import (
    Config,
    migrate,
    Group,
    Member,
    Lesson,
    Role,
    Topic,
    LessonMember
)


migrate()  # TODO: Comment this line in production

app = FastAPI(
    title="Stars Portal API - ",  # TODO: Change the title and description
    description="""
    Description
    """,
    version="0.0.1",
)

db_crud_router = APIRouter()


# def init_pydantic_models():
pydantic_models = generate_pydantic_models(
    Config.BASE.metadata,
    exclude_tables=["lesson_members"]
)

from . import routes

for router in generate_crud_routers(pydantic_models):
    db_crud_router.include_router(router)


# logger.info(router)
# exit()

# init_pydantic_models()
# app.include_router(appeals_router)
app.include_router(db_crud_router)
PATH_LIST = [x.path for x in app.routes]

def base_url_endpoint(url):
    return url.split("/")[1]

@app.middleware("http")
async def add_wrong_request_path_redirect(request: Request, call_next):
    print(request.headers)
    url = request.url.path
    if base_url_endpoint(url) in [base_url_endpoint(x) for x in PATH_LIST]:
        response = await call_next(request)
        logger.info(f"{request.client} : {request.url} -> {response.status_code}")
    else:
        #  response = RedirectResponse(PATH_LIST[-1])
         response = RedirectResponse("/docs")
    return response


