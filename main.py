import uuid
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from voice_registry import get_all_voices
from categories import ALL_PRESETS, CATEGORY_PLAN
from security import check_rate_limit, validate_text_input
from audio_service import get_audio_file_path, cleanup_expired_audio, AUDIO_EXPIRY_SECONDS
from tts_engine import synthesize_speech

JOBS = {}
CONCURRENCY_LOCK = asyncio.Semaphore(2)

async def periodic_cleanup():
    while True:
        cleanup_expired_audio()
        await asyncio.sleep(60)

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(periodic_cleanup())
    yield
    task.cancel()

app = FastAPI(title="AI Voice Generator API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    text: str = Field(..., min_length=2, max_length=3000)
    voice_id: str = Field(default="lira_natural")
    language: str = Field(default="hi")
    unlocked_minutes: int = Field(default=4, ge=1, le=5)

async def _process_tts_job(
    job_id: str,
    clean_text: str,
    language: str,
    speed: float,
    base_voice: str,
    category: str,
):
    JOBS[job_id]["status"] = "processing"
    async with CONCURRENCY_LOCK:
        try:
            audio_id = await asyncio.to_thread(
                synthesize_speech,
                clean_text,
                language,
                speed,
                base_voice,
                category,
            )
            JOBS[job_id]["status"] = "completed"
            JOBS[job_id]["audio_id"] = audio_id
            JOBS[job_id]["audio_url"] = f"/audio/{audio_id}"
            JOBS[job_id]["expires_in_seconds"] = AUDIO_EXPIRY_SECONDS
        except Exception:
            JOBS[job_id]["status"] = "failed"
            JOBS[job_id]["error"] = "TTS engine temporarily unavailable. Please try again."

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "AI Voice Generator API", "total_presets": len(ALL_PRESETS)}

@app.get("/voices")
def list_voices():
    return {"real_voices": get_all_voices(), "presets": list(ALL_PRESETS.values())}

@app.get("/categories")
def list_categories():
    grouped = {}
    for preset in ALL_PRESETS.values():
        grouped.setdefault(preset["category"], []).append(preset)
    return {
        "summary": [{"category": name, "count": count} for name, count in CATEGORY_PLAN],
        "total_presets": len(ALL_PRESETS),
        "categories": grouped,
    }

@app.post("/generate")
async def create_generation_job(req: GenerateRequest, request: Request, background_tasks: BackgroundTasks):
    check_rate_limit(request)
    if req.voice_id not in ALL_PRESETS:
        raise HTTPException(status_code=404, detail="Invalid voice_id")

    preset = ALL_PRESETS[req.voice_id]
    clean_text = validate_text_input(req.text, req.unlocked_minutes)

    job_id = uuid.uuid4().hex
    JOBS[job_id] = {"job_id": job_id, "status": "queued", "voice_id": req.voice_id}

    background_tasks.add_task(
        _process_tts_job,
        job_id,
        clean_text,
        req.language or preset["language"],
        preset["speed"],
        preset["base_voice"],
        preset["category"],
    )
    return {"job_id": job_id, "status": "queued", "poll_url": f"/jobs/{job_id}"}

@app.get("/jobs/{job_id}")
def get_job_status(job_id: str):
    if job_id not in JOBS:
        raise HTTPException(status_code=404, detail="Job not found")
    return JOBS[job_id]

@app.get("/audio/{audio_id}")
def download_audio(audio_id: str):
    path = get_audio_file_path(audio_id)
    if not path:
        raise HTTPException(status_code=404, detail="Audio expired or not found")
    return FileResponse(path, media_type="audio/wav", filename=audio_id)