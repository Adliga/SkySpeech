import numpy as np


def apply_audio_effects(wav: np.ndarray, sr: int, pitch_shift: float = 1.0) -> np.ndarray:
    if pitch_shift != 1.0:
        import librosa
        n_steps = 12 * np.log2(pitch_shift)
        wav = librosa.effects.pitch_shift(y=wav, sr=sr, n_steps=n_steps)

    return wav
