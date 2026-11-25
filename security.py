import time
from collections import defaultdict
from fastapi import HTTPException, Request

RATE_LIMIT_WINDOW = 60
MAX_REQUESTS_PER_WINDOW = 10
_request_log = defaultdict(list)

MAX_TEXT_CHARS = 3000
MIN_TEXT_CHARS = 2

def check_rate_limit(request: Request):
    client_ip = request.client.host if request.client else "unknown"
    now = time.time()
    _request_log[client_ip] = [t for t in _request_log[client_ip] if now - t < RATE_LIMIT_WINDOW]
    if len(_request_log[client_ip]) >= MAX_REQUESTS_PER_WINDOW:
        raise HTTPException(status_code=429, detail="Too many requests. Please wait 1 minute.")
    _request_log[client_ip].append(now)

def validate_text_input(text: str, unlocked_minutes: int = 4) -> str:
    cleaned = text.strip()
    if len(cleaned) < MIN_TEXT_CHARS:
        raise HTTPException(status_code=400, detail="Text is too short.")
    allowed_chars = min(max(unlocked_minutes, 1), 5) * 600
    if len(cleaned) > allowed_chars or len(cleaned) > MAX_TEXT_CHARS:
        raise HTTPException(
            status_code=400,
            detail=f"Text exceeds {allowed_chars} characters limit for {unlocked_minutes} minute(s)."
        )
    return cleaned