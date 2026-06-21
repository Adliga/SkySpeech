import io
import traceback

import numpy as np
import soundfile as sf
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel

from model_loader import infer_synthesize, get_voice_ref
from utils.audio import apply_audio_effects

router = APIRouter()


class SynthesizeRequest(BaseModel):
    text: str
    voice_id: str = "child"
    rate: float = 1.0
    pitch: float = 1.0


@router.post("/synthesize")
def synthesize(req: SynthesizeRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text is empty")

    ref = get_voice_ref(req.voice_id)
    if ref is None:
        raise HTTPException(
            status_code=400,
            detail=f"Voice '{req.voice_id}' has no reference audio.",
        )

    ref_audio_path, ref_text = ref

    try:
        wav, sr = infer_synthesize(
            ref_audio_path=ref_audio_path,
            ref_text=ref_text,
            gen_text=req.text,
            speed=req.rate,
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    if wav is None:
        raise HTTPException(status_code=500, detail="Model returned no audio")

    if req.pitch != 1.0:
        try:
            wav = apply_audio_effects(wav, sr, pitch_shift=req.pitch)
        except Exception as e:
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Audio effects error: {e}")

    buf = io.BytesIO()
    sf.write(buf, wav, sr, format="wav")
    buf.seek(0)

    return Response(content=buf.getvalue(), media_type="audio/wav")
