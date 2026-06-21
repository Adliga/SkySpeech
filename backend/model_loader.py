import os
import json
import uuid
import warnings
from pathlib import Path

import numpy as np
import torch
import soundfile as sf

warnings.filterwarnings("ignore")

DATA_DIR = Path(__file__).parent / "data"
VOICES_DIR = DATA_DIR / "voices"
CLONED_DIR = DATA_DIR / "cloned"
VOICES_INDEX = DATA_DIR / "voices_index.json"

TARGET_SR = 24000

STANDARD_VOICE_ICONS = {
    "child": "",
    "female_3": "",
    "speaker_3": "",
    "speaker_4": "",
    "speaker_5": "",
}

_tts_instance = None
_voices_index = None


def _patch_torchaudio():
    import torchaudio as ta
    _orig = ta.load

    def _sf_load(path, *args, **kwargs):
        audio_np, sr = sf.read(path, dtype="float32")
        if audio_np.ndim == 1:
            audio_np = audio_np[np.newaxis, :]
        else:
            audio_np = audio_np.T
        return torch.from_numpy(audio_np), sr

    if ta.load is not _sf_load:
        ta.load = _sf_load


def get_voices_index():
    global _voices_index
    if _voices_index is None:
        if VOICES_INDEX.exists():
            with open(VOICES_INDEX, "r", encoding="utf-8") as f:
                _voices_index = json.load(f)
        else:
            _voices_index = {"standard": {}, "cloned": {}}
            save_voices_index()
    return _voices_index


def save_voices_index():
    global _voices_index
    with open(VOICES_INDEX, "w", encoding="utf-8") as f:
        json.dump(_voices_index, f, ensure_ascii=False, indent=2)


def init_standard_voices():
    index = get_voices_index()
    wav_files = sorted(VOICES_DIR.glob("*.wav"))

    for wav in wav_files:
        voice_id = wav.stem
        if voice_id in index["standard"] and index["standard"][voice_id].get("audio_path"):
            continue

        voice_dir = VOICES_DIR / voice_id
        voice_dir.mkdir(exist_ok=True)

        audio_np, sr = sf.read(str(wav), dtype="float32")
        if audio_np.ndim > 1:
            audio_np = np.mean(audio_np, axis=1)

        out_path = str(voice_dir / "ref_24k.wav")
        sf.write(out_path, audio_np, TARGET_SR)

        index["standard"][voice_id] = {
            "audio_path": out_path,
            "ref_text": "",
        }
        save_voices_index()


def get_tts():
    global _tts_instance
    if _tts_instance is None:
        _patch_torchaudio()
        from TTS.api import TTS
        _tts_instance = TTS(
            "tts_models/multilingual/multi-dataset/xtts_v2",
            gpu=False,
        )
    return _tts_instance


def infer_synthesize(
    ref_audio_path: str,
    ref_text: str,
    gen_text: str,
    speed: float = 1.0,
) -> tuple:
    tts = get_tts()
    wav = tts.tts(
        text=gen_text,
        speaker_wav=ref_audio_path,
        language="ru",
    )
    wav = np.array(wav, dtype=np.float32)

    if speed != 1.0:
        import librosa
        wav = librosa.effects.time_stretch(y=wav, rate=speed)

    return wav, TARGET_SR


def get_voice_ref(voice_id: str):
    index = get_voices_index()
    entry = (
        index.get("standard", {}).get(voice_id)
        or index.get("cloned", {}).get(voice_id)
    )
    if not entry:
        return None
    ap = entry.get("audio_path")
    if not ap or not os.path.exists(ap):
        return None
    return ap, entry.get("ref_text") or "."


def register_cloned_voice(raw_audio_path: str, display_name: str | None = None) -> dict:
    voice_id = f"cloned_{uuid.uuid4().hex[:8]}"
    voice_dir = CLONED_DIR / voice_id
    voice_dir.mkdir(parents=True, exist_ok=True)

    audio_np, sr = sf.read(raw_audio_path, dtype="float32")
    if audio_np.ndim > 1:
        audio_np = np.mean(audio_np, axis=1)

    ref_path = str(voice_dir / "ref_24k.wav")
    sf.write(ref_path, audio_np, TARGET_SR)

    index = get_voices_index()
    n = len(index["cloned"]) + 1
    index["cloned"][voice_id] = {
        "audio_path": ref_path,
        "ref_text": "",
        "displayName": display_name or f"Мой голос {n}",
    }
    save_voices_index()

    if raw_audio_path.startswith(str(CLONED_DIR / "_raw")):
        os.remove(raw_audio_path)

    return {"voice_id": voice_id}
