from fastapi import APIRouter

from model_loader import get_voices_index, init_standard_voices, STANDARD_VOICE_ICONS

router = APIRouter()

VOICE_DISPLAY_NAMES = {
    "child": "Детский",
    "female_3": "Женский",
    "speaker_3": "Мужской_1",
    "speaker_4": "Мужской_2",
    "speaker_5": "Мужской_3",
}


@router.post("/voices/standard")
async def get_standard_voices():
    init_standard_voices()
    index = get_voices_index()
    voices = []

    for vid, ventry in index["standard"].items():
        voices.append({
            "name": vid,
            "displayName": VOICE_DISPLAY_NAMES.get(vid, vid),
            "icon": "",
            "ready": bool(ventry.get("audio_path")),
        })

    return {"voices": voices}
