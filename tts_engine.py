import os
from gradio_client import Client
from audio_service import save_temp_wav

HF_TOKEN = os.getenv("HF_TOKEN", None)

def synthesize_speech(text: str, language: str, speed: float = 1.0) -> str:
    client = Client("mrfakename/E2-F5-TTS", hf_token=HF_TOKEN if HF_TOKEN else None)
    result = client.predict(
        ref_audio_input=None,
        ref_text_input="",
        gen_text_input=text,
        remove_silence=True,
        api_name="/basic_tts",
    )
    raw_wav_path = result[0] if isinstance(result, (list, tuple)) else result
    return save_temp_wav(raw_wav_path)