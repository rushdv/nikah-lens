"""
NikahLens FastAPI Application.
Privacy-Conscious Matrimonial Profile Discovery Engine Backend.
"""

import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.session import init_db
from database.seed.seed_data import run_seed
from apps.api.routers import (
    health, profiles, search, search_profiles, shortlists, notes, sources, duplicates
)

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("nikah_lens")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing NikahLens database schema...")
    init_db()
    # Check if database has profiles, if not auto-seed synthetic profiles
    from database.session import SessionLocal
    from database.models import ProfileModel
    db = SessionLocal()
    try:
        count = db.query(ProfileModel).count()
        if count == 0:
            logger.info("Database empty, running initial synthetic seed...")
            run_seed()
    finally:
        db.close()
    yield
    logger.info("NikahLens backend shutting down...")


app = FastAPI(
    title="NikahLens API",
    description="Privacy-Conscious Matrimonial Profile Discovery Engine",
    version="0.1.0",
    lifespan=lifespan
)

# CORS configuration
origins_str = os.getenv("API_CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")
origins = [o.strip() for o in origins_str.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health endpoint (available at both root and api prefix)
app.include_router(health.router)

# API v1 endpoints
api_v1_prefix = "/api/v1"
app.include_router(profiles.router, prefix=api_v1_prefix)
app.include_router(search.router, prefix=api_v1_prefix)
app.include_router(search_profiles.router, prefix=api_v1_prefix)
app.include_router(shortlists.router, prefix=api_v1_prefix)
app.include_router(notes.router, prefix=api_v1_prefix)
app.include_router(sources.router, prefix=api_v1_prefix)
app.include_router(duplicates.router, prefix=api_v1_prefix)


@app.get("/")
def root():
    return {
        "app": "NikahLens",
        "tagline": "Privacy-Conscious Matrimonial Profile Discovery Engine",
        "docs": "/docs",
        "api_v1": "/api/v1"
    }
