from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.infrastructure.database import Base, engine
from app.api.routes import upload, otp, temple, user, forgot_password

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user.router, prefix="/user")
app.include_router(temple.router, prefix="/temple")
app.include_router(forgot_password.router, prefix="/forgot-password")
app.include_router(upload.router, prefix="/upload")
app.include_router(otp.router, prefix="/otp")

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/")
def home():
    return {"message": "Backend Running"}
