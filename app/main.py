from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.infrastructure.database import engine, Base
from app.api.routes import upload, otp, temple
from app.api.routes.user import router as user_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_router, prefix="/user")
app.include_router(upload.router, prefix="/upload")
app.include_router(otp.router, prefix="/otp")
app.include_router(temple.router, prefix="/temple")

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/")
def home():
    return {"message": "Clean Architecture Backend Running"}
