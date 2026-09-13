from fastapi import FastAPI

from api.vision import router as vision_router
from api.ocr import router as ocr_router
from api.voice import router as voice_router
from api.emergency import router as emergency_router


app = FastAPI(
    title="SeeForMe AI Backend",
    description="Backend API for SeeForMe accessibility assistant",
    version="1.0.0"
)


app.include_router(vision_router)
app.include_router(ocr_router)
app.include_router(voice_router)
app.include_router(emergency_router)


@app.get("/")
def home():
    return {
        "message": "SeeForMe AI Backend is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }