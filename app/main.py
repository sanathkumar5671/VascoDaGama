# app/main.py
from fastapi import FastAPI
from app.controllers.voice_controller import router as voice_router
from app.controllers.recommendation_controller import router as rec_router

app = FastAPI(title="Restaurant Recommendation MVP")

# Include voice and recommendation endpoints
app.include_router(voice_router, prefix="/voice")
app.include_router(rec_router, prefix="/recommendation")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
