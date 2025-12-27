import os
import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("Missing TELEGRAM_BOT_TOKEN")

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
FILE_BASE = f"https://api.telegram.org/file/bot{BOT_TOKEN}"

app = FastAPI()

# SIMPLE IN-MEMORY CACHE
FILE_CACHE = {}

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/video/{file_id}")
def get_video_url(file_id: str):
    # cache hit
    if file_id in FILE_CACHE:
        return FILE_CACHE[file_id]

    # call Telegram getFile
    r = requests.get(f"{BASE_URL}/getFile", params={"file_id": file_id})
    data = r.json()

    if not data.get("ok"):
        raise HTTPException(status_code=400, detail="Invalid file_id")

    file_path = data["result"]["file_path"]
    video_url = f"{FILE_BASE}/{file_path}"

    response = {"video_url": video_url}
    FILE_CACHE[file_id] = response

    return JSONResponse(response)
