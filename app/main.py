from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
import logging

from app.infrastructure.database import Base, engine, test_connection
from app.api.routes import upload, otp, temple, user, forgot_password

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting app...")
    try:
        # Test database connection
        if test_connection():
            # Create tables
            Base.metadata.create_all(bind=engine)
            logger.info("✅ Database tables created successfully")
        else:
            logger.warning("⚠️ Database connection failed - tables not created")
    except Exception as e:
        logger.error(f"❌ Database initialization error: {e}")

    yield


app = FastAPI(
    title="Temple Backend API",
    description="FastAPI backend for temple management system",
    version="1.0.0",
    lifespan=lifespan
)

# Routers
app.include_router(user.router, prefix="/user", tags=["User Management"])
app.include_router(temple.router, prefix="/temple", tags=["Temple Management"])
app.include_router(forgot_password.router, prefix="/forgot-password", tags=["Password Recovery"])
app.include_router(upload.router, prefix="/upload", tags=["File Upload"])
app.include_router(otp.router, prefix="/otp", tags=["OTP Services"])

# Upload folder
if not os.path.exists("uploads"):
    os.makedirs("uploads")
    logger.info("📁 Created uploads directory")

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/", tags=["Health"])
def home():
    return {
        "message": "Temple Backend API Running",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint"""
    db_status = "healthy" if test_connection() else "unhealthy"
    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "database": db_status,
        "timestamp": "2026-04-18"  # Would use datetime.now() in real implementation
    }