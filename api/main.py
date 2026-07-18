from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

from api.database import Base, engine
import api.models

from api.detect import router as detect_router
from api.reports import router as reports_router

# Create database tables
Base.metadata.create_all(bind=engine)

# Create results folder if it doesn't exist
os.makedirs("results", exist_ok=True)

app = FastAPI(
    title="Egg Inspection API",
    description="Backend service for egg tray inspection",
    version="1.0"
)

# Serve annotated images
app.mount("/results", StaticFiles(directory="results"), name="results")

# Register API routes
app.include_router(detect_router)
app.include_router(reports_router)


def home():
    return {
        "message": "Welcome to the Egg Inspection API",
        "endpoints": [
            "POST /detect",
            "GET /reports/{id}",
            "GET /reports/summary"
        ]
    }


def health():
    return {
        "status": "Server is running"
    }


app.add_api_route("/", home, methods=["GET"])
app.add_api_route("/health", health, methods=["GET"])