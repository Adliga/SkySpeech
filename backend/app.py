from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from routes.synthesize import router as synthesize_router
from routes.clone import router as clone_router
from routes.voices import router as voices_router

app = FastAPI(title="SkySpeech API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(synthesize_router)
app.include_router(clone_router)
app.include_router(voices_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
