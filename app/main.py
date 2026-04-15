from fastapi import FastAPI
from app.api.routes.auth import router as auth_router
from app.infrastructure.database import engine, Base
from app.api.routes import upload
from fastapi.staticfiles import StaticFiles
from app.api.routes import otp
from app.api.routes import temple

app = FastAPI()

# ✅ CREATE TABLES
Base.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix="/auth")
app.include_router(upload.router, prefix="/upload")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.include_router(otp.router, prefix="/otp")
app.include_router(temple.router, prefix="/temple")

@app.get("/")
def home():
    return {"message": "Clean Architecture Backend Running 🚀"}