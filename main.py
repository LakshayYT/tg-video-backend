import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

# ========================
# Environment variables
# ========================
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
GROUP_USERNAME = os.getenv("GROUP_USERNAME")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")  # +91XXXXXXXXXX

# ========================
# App & Telegram client
# ========================
app = FastAPI()
client = TelegramClient("session", API_ID, API_HASH)

# ========================
# Startup: login to Telegram
# ========================
@app.on_event("startup")
async def startup():
    await client.start(phone=PHONE_NUMBER)
    print("✅ Telegram client started")

# ========================
# List videos
# ========================
@app.get("/videos")
async def list_videos():
    entity = await client.get_entity(GROUP_USERNAME)

    history = await client(GetHistoryRequest(
        peer=entity,
        limit=50,
        offset_date=None,
        offset_id=0,
        max_id=0,
        min_id=0,
        add_offset=0,
        hash=0
    ))

    videos = []
    for msg in history.messages:
        if msg.video:
            videos.append({
                "id": msg.id,
                "title": msg.message or f"Video {msg.id}",
                "size_mb": round(msg.video.size / (1024 * 1024), 2)
            })

    return JSONResponse(videos)

# ========================
# Stream video
# ========================
@app.get("/stream/{msg_id}")
async def stream_video(msg_id: int):
    entity = await client.get_entity(GROUP_USERNAME)
    msg = await client.get_messages(entity, ids=msg_id)

    if not msg or not msg.video:
        raise HTTPException(status_code=404, detail="Video not found")

    async def video_generator():
        async for chunk in client.iter_download(
            msg.video,
            chunk_size=1024 * 1024  # 1 MB chunks
        ):
            yield chunk

    return StreamingResponse(
        video_generator(),
        media_type="video/mp4"
    )
