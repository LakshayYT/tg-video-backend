import os
import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHANNEL_USERNAME = "project45lakshya"   # WITHOUT @

if not BOT_TOKEN:
    raise RuntimeError("Missing TELEGRAM_BOT_TOKEN")

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
FILE_BASE = f"https://api.telegram.org/file/bot{BOT_TOKEN}"

app = FastAPI()

# simple in-memory cache: message_id -> video_url
CACHE = {}

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/video/{message_id}")
def get_video_by_message_id(message_id: int):

    # cache hit
    if message_id in CACHE:
        return CACHE[message_id]

    # 1️⃣ get message from channel
    r = requests.get(
        f"{BASE_URL}/getMessage",
        params={
            "chat_id": f"@{CHANNEL_USERNAME}",
            "message_id": message_id
        },
        timeout=10
    )

    data = r.json()
    if not data.get("ok"):
        raise HTTPException(status_code=404, detail="Message not found")

    message = data["result"]

    if "video" not in message:
        raise HTTPException(status_code=404, detail="Message has no video")

    # 2️⃣ bot-native file_id
    file_id = message["video"]["file_id"]

    # 3️⃣ get file_path
    r2 = requests.get(
        f"{BASE_URL}/getFile",
        params={"file_id": file_id},
        timeout=10
    )

    data2 = r2.json()
    if not data2.get("ok"):
        raise HTTPException(status_code=400, detail="getFile failed")

    file_path = data2["result"]["file_path"]
    video_url = f"{FILE_BASE}/{file_path}"

    response = {"video_url": video_url}
    CACHE[message_id] = response

    return JSONResponse(response)
