import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.messages import GetHistoryRequest

# =========================
# Environment Variables
# =========================

try:
    API_ID = int(os.environ["API_ID"])
    API_HASH = os.environ["API_HASH"]
    GROUP_USERNAME = os.environ["GROUP_USERNAME"]
    SESSION_STRING = os.environ["SESSION_STRING"]
except KeyError as e:
    raise RuntimeError(f"Missing required env variable: {e}")

# =========================
# Telegram Client
# =========================

client = TelegramClient(
    StringSession(SESSION_STRING),
    API_ID,
    API_HASH,
    connection_retries=5,
    retry_delay=2,
    auto_reconnect=True
)

# =========================
# FastAPI Lifespan
# =========================

@asynccontextmanager
async def lifespan(app: FastAPI):
    await client.start()
    print("✅ Telegram client connected")
    yield
    await client.disconnect()
    print("🛑 Telegram client disconnected")

app = FastAPI(lifespan=lifespan)

# =========================
# Routes
# =========================

@app.get("/")
async def root():
    return {"status": "ok", "service": "telegram-video-streamer"}

@app.get("/videos")
async def list_videos():
    try:
        entity = await client.get_entity(GROUP_USERNAME)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid group/channel username")

    history = await client(
        GetHistoryRequest(
            peer=entity,
            limit=2000,
            offset_date=None,
            offset_id=0,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0
        )
    )

    videos = []
    for msg in history.messages:
        if msg.video:
            videos.append({
                "id": msg.id,
                "title": msg.message or f"Video {msg.id}",
                "size_mb": round(msg.video.size / (1024 * 1024), 2)
            })

    return JSONResponse(videos)

@app.get("/stream/{msg_id}")
async def stream_video(msg_id: int):
    entity = await client.get_entity(GROUP_USERNAME)
    msg = await client.get_messages(entity, ids=msg_id)

    if not msg or not msg.video:
        raise HTTPException(status_code=404, detail="Video not found")

    async def video_generator():
        async for chunk in client.iter_download(
            msg.video,
            chunk_size=256 * 1024  # Railway-safe chunk size
        ):
            yield chunk

    return StreamingResponse(
        video_generator(),
        media_type="video/mp4"
    )
