from fastapi import FastAPI
from contextlib import asynccontextmanager
from Books.routes import router as books_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application Start Up")
    yield
    print("Application Shut Down")

tags_metadata = [
    {
        "name": "personal library",
        "description": "Operations related to the personal library management",
        "externalDocs": {
            "description": "more about personal library",
            "url": "http://example.com/docs/personal_library",
        },
    }
]

app = FastAPI(
    title="Personal Library",
    description="An environment for managing your personal reading and books",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Mehdi Ostad",
        "url": "http://github.com/MehdiOstad1212",
        "email": "wishtree1248@gmail.com",
    },
    license_info={
        "name": "MIT",
    },
    lifespan=lifespan,
    openapi_tags=tags_metadata,
)

app.include_router(books_routes, prefix = "/api/v1")