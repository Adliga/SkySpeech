import os
import shutil
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException

from model_loader import register_cloned_voice, CLONED_DIR

router = APIRouter()


@router.post("/clone")
async def clone_voice(audio: UploadFile = File(...)):
    if not audio or not audio.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    ext = os.path.splitext(audio.filename)[1].lower()
    if ext not in (".wav", ".mp3"):
        raise HTTPException(status_code=400, detail="Only WAV and MP3 files are supported")

    raw_dir = CLONED_DIR / "_raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    raw_path = raw_dir / f"upload_{len(os.listdir(raw_dir))}{ext}"

    with open(raw_path, "wb") as f:
        shutil.copyfileobj(audio.file, f)

    result = register_cloned_voice(str(raw_path), audio.filename)

    return {"voice_id": result["voice_id"]}
