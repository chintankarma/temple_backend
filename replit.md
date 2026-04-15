# Clean Architecture FastAPI Backend

## Overview
A FastAPI-based backend built with Clean Architecture principles. Provides user authentication (including OTP), file uploads, and temple management features.

## Tech Stack
- **Language:** Python 3.12
- **Framework:** FastAPI with Uvicorn ASGI server
- **Database:** SQLite (via SQLAlchemy ORM) — stored in `test.db`
- **Auth:** JWT tokens (`python-jose`) + bcrypt password hashing (`passlib`)
- **Validation:** Pydantic v2

## Project Layout
```
app/
  api/routes/       # FastAPI route definitions (auth, otp, temple, upload)
  core/             # Security (JWT/hashing) and OTP store
  domain/
    models/         # SQLAlchemy models (User, Temple)
    services/       # Business logic (AuthService, TempleService)
  infrastructure/
    database.py     # SQLite engine setup
    repositories/   # Data access layer
  schemas/          # Pydantic request/response models
  main.py           # App entry point
uploads/            # Stored file uploads (served as static files)
requirements.txt    # Python dependencies
test.db             # SQLite database file
```

## Running the App
- Workflow: `uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload`
- API docs available at `/docs` (Swagger UI)

## Key Endpoints
- `GET /` — Health check
- `POST /auth/...` — Authentication routes
- `POST /otp/...` — OTP routes
- `POST /upload/...` — File upload routes
- `GET /temple/...` — Temple management routes
- `GET /uploads/{filename}` — Static file serving
