import os
import time
import uuid
import shutil

TEMP_AUDIO_DIR = "temp_audio"
AUDIO_EXPIRY_SECONDS = int(os.getenv("AUDIO_EXPIRY_SECONDS", "600"))
os.makedirs(TEMP_AUDIO_DIR, exist_ok=True)

def save_temp_wav(source_path: str) -> str:
    audio_id = f"{uuid.uuid4().hex}.wav"
    dest_path = os.path.join(TEMP_AUDIO_DIR, audio_id)
    shutil.copy(source_path, dest_path)
    return audio_id

def get_audio_file_path(audio_id: str) -> str | None:
    if not audio_id.endswith(".wav") or "/" in audio_id or "\\" in audio_id:
        return None
    full_path = os.path.join(TEMP_AUDIO_DIR, audio_id)
    if os.path.exists(full_path):
        return full_path
    return None

def cleanup_expired_audio():
    now = time.time()
    for fname in os.listdir(TEMP_AUDIO_DIR):
        fpath = os.path.join(TEMP_AUDIO_DIR, fname)
        if os.path.isfile(fpath) and (now - os.path.getmtime(fpath)) > AUDIO_EXPIRY_SECONDS:
            try:
                os.remove(fpath)
            except OSError:
                pass