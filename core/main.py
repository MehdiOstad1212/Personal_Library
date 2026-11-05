from fastapi import FastAPI, status, HTTPException
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from Books.routes import router as books_routes
from users.routes import router as users_routes
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError

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
app.include_router(users_routes, prefix = "/api/v1")

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    error_response = {
        "error": True,
        "status_code": exc.status_code,
        "detail": str(exc.detail)
    }
    return JSONResponse(status_code = exc.status_code, content = error_response)

@app.exception_handler(RequestValidationError)
async def http_validation_exception_handler(request, exc):
    error_response = {
        "error": True,
        "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
        "detail": "there was a problem with your form request",
        "content": exc.errors()
    }
    return JSONResponse(status_code = status.HTTP_422_UNPROCESSABLE_CONTENT, 
                        content = error_response)

@app.get('/')
def root():
    return JSONResponse(content = {'message': 'Hello World!'}, status_code = status.HTTP_202_ACCEPTED)