from fastapi import APIRouter

from app.api.api_v1.endpoints import dataset

api_router = APIRouter()
api_router.include_router(dataset.router, prefix='/datasets', tags=['datasets'])
