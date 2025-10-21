from fastapi import APIRouter
from src.config.logger import logger


logger = logger("health")

router = APIRouter(
    tags=["Health Check"],
)

@router.get('/health')
async def health_check() -> dict:
    logger.info("Health check endpoint called")
    return {"health": True}