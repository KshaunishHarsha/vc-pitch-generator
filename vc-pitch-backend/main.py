"""
VC Pitch Generator - FastAPI Backend
Main application entry point
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import from folders
from config import settings
from routes.pitch import router as pitch_router
from middleware.rate_limit import rate_limit_middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown"""
    logger.info("=" * 50)
    logger.info("🚀 VC Pitch Generator API Starting")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Rate limiting: {'Enabled' if settings.RATE_LIMIT_ENABLED else 'Disabled'}")
    logger.info(f"Allowed origins: {settings.ALLOWED_ORIGINS}")
    logger.info("=" * 50)
    yield
    logger.info("🛑 VC Pitch Generator API Shutting Down")


# Initialize FastAPI app
app = FastAPI(
    title="VC Pitch Generator API",
    description="Transform any startup idea into a buzzword-heavy VC pitch",
    version="1.0.0",
    lifespan=lifespan
)

from starlette.middleware.base import BaseHTTPMiddleware

# Rate limiting middleware (must be added BEFORE CORS so it runs inner)
app.add_middleware(BaseHTTPMiddleware, dispatch=rate_limit_middleware)

# CORS Middleware (must be added LAST so it runs outermost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(pitch_router)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API info"""
    return {
        "message": "VC Pitch Generator API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "examples": "/api/examples",
        "generate": "/api/generate-pitch"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "vc-pitch-generator",
        "version": "1.0.0"
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "details": str(exc) if settings.DEBUG else "An unexpected error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )