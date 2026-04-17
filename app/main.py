from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from app.infrastructure.database import Base, engine
from app.api.routes import upload, otp, temple, user, forgot_password


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting app...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ DB Connected (Neon)")
    except Exception as e:
        print("❌ DB Error:", e)

    yield


app = FastAPI(lifespan=lifespan)

# Routers
app.include_router(user.router, prefix="/user")
app.include_router(temple.router, prefix="/temple")
app.include_router(forgot_password.router, prefix="/forgot-password")
app.include_router(upload.router, prefix="/upload")
app.include_router(otp.router, prefix="/otp")

# Upload folder
if not os.path.exists("uploads"):
    os.makedirs("uploads")

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/")
def home():
    return {"message": "Backend Running"}