import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.environ.get("SUPABASE_DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("SUPABASE_DATABASE_URL environment variable is not set")

# Force IPv4 and use connection args suitable for Supabase pooler
engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"},
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()
