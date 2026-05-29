"""API v1 router configuration.

This module sets up the main API router and includes all sub-routers for different
endpoints like authentication and chatbot functionality.
"""

from fastapi import APIRouter

from app.api.v1.auth import router as legacy_auth_router
from app.api.v1.chatbot import router as chatbot_router
from app.core.logging import logger
from app.api.routes.auth import router as zoho_auth_router
api_router = APIRouter()

# Include routers
api_router.include_router(legacy_auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(chatbot_router, prefix="/chatbot", tags=["chatbot"])
api_router.include_router(zoho_auth_router)
@api_router.get("/health")
async def health_check():
    """Health check endpoint.

    Returns:
        dict: Health status information.
    """
    logger.info("health_check_called")
    return {"status": "healthy", "version": "1.0.0"}
