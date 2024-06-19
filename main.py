from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from api.routers import api_router

app = FastAPI(
    title = settings.PROJECT_NAME,
    version = settings.PROJECT_VERSION
)

origins = [
    'http://localhost:5173'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["GET", "POST", "PUT"],
    allow_headers = ["*"]
)

app.include_router(api_router, prefix='/api/v1')

