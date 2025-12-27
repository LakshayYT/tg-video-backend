import os
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse, RedirectResponse
from pyrogram import Client

app = FastAPI()

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
# You MUST set these in Railway Variables for the streaming to work
# Get them from https://my.telegram.org/apps
API_ID = int(os.getenv("API_ID", "25553656")) 
API_HASH = os.getenv("API_HASH", "871b96c886915152865d49673a6e8e86")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8416192372:AAEB5qfAW2ExFvZquF-uTo03-kSPBSryLtk")

# Initialize Pyrogram Client
client = Client("my_bot_session", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, in_memory=True)

# ---------------------------------------------------------
# EMBEDDED DATA
# ---------------------------------------------------------
lectures_db = [
    {"id": 1, "telegram_file_id": "BAACAgUAAxkBAAEZuFVpTwpkfL2UU6FuC7i8aGMJeyV7KAAC2hwAAgKwgVWA-wAB7t22CMM2BA", "railway_url": None},
    {"id": 2, "telegram_file_id": "BAACAgUAAxkBAAEZuF1pTwp_pbPOF4DeqQ88mTHcLqEzawAC-h8AAkHEmVWMRFEuyBBrfTYE", "railway_url": None},
    {"id": 3, "telegram_file_id": "BAACAgUAAxkBAAEZuF9pTwqFXKRZXjRwNsiGbwXwxVSZxAACsBYAArX5qFUEdDliKrLKWjYE", "railway_url": None},
    {"id": 4, "telegram_file_id": "BAACAgUAAxkBAAEZuIdpTwr7-skBV6oim5nYIOSoaWeayAACqBsAAslR0VV3lnyC2JT57DYE", "railway_url": None},
    {"id": 5, "telegram_file_id": "BAACAgUAAxkBAAEZuJdpTwsrAR9ulQHeJgkAAYYJxwRbO6oAAucaAAItq-BVuf9on83oTos2BA", "railway_url": None},
    {"id": 6, "telegram_file_id": "BAACAgUAAxkBAAEZuLdpTwtyRRqdkWoYru6tldmkBTNQYQAC3xoAAjY6IVbT5Jxw83XfczYE", "railway_url": None},
    {"id": 7, "telegram_file_id": "BAACAgUAAxkBAAEZuMlpTwuWmJaKObvLk1kMwr_MvcI-4wAC3x8AAkXNSVYCgd_j0QnBOzYE", "railway_url": None},
    {"id": 8, "telegram_file_id": "BAACAgUAAxkBAAEZuFlpTwpxEdNbaIWOddpz_p1WPZnGbwACJBoAApGOkVUfK4saL_tnjzYE", "railway_url": None},
    {"id": 9, "telegram_file_id": "BAACAgUAAxkBAAEZuHVpTwrMXFu7Hab0jpdkU9vHmAVYSgACeRoAAtMxuFXLd5v3FChGxDYE", "railway_url": None},
    {"id": 10, "telegram_file_id": "BAACAgUAAxkBAAEZuHtpTwrcsO02X9_7vyuRvPQxwAvbQAACzhQAAmYRyVXBJHcuJVr1AjYE", "railway_url": None},
    {"id": 11, "telegram_file_id": "BAACAgUAAxkBAAEZuKlpTwtRYZ-cjbf2c0aKTXJlJ0wFywACDR8AAnWlEFZ8H15JFJophTYE", "railway_url": None},
    {"id": 12, "telegram_file_id": "BAACAgUAAxkBAAEZuL1pTwt-oNpRPnMDEm-JFNwPVFZv9AACahoAAhvbKFbWbUN5L3F0wTYE", "railway_url": None},
    {"id": 13, "telegram_file_id": "BAACAgUAAxkBAAEZuM1pTwue7S94gWsCpqflt0jnLu4viAADLAAC-AZYVjIokq7Uz8STNgQ", "railway_url": None},
    {"id": 14, "telegram_file_id": "BAACAgUAAxkBAAEZuIVpTwr3Ke7fuZoW-3DWcXg2h4SzQgAC8BsAAslR0VWtaUFH2oUv0TYE", "railway_url": None},
    {"id": 15, "telegram_file_id": "BAACAgUAAxkBAAEZuLVpTwtuSJQBnMt6qhmUI8fNSgSkIwAC3BoAAjY6IVZj-anHqU8uljYE", "railway_url": None},
    {"id": 16, "telegram_file_id": "BAACAgUAAxkBAAEZuMdpTwuSfIeQRFUE9R_sb_SvPPN5SwAC3R8AAkXNSVbxB-a-jWVcGzYE", "railway_url": None},
    {"id": 17, "telegram_file_id": "BAACAgUAAxkBAAEZuNNpTwupUEudPGQT-euB0Izi9nUrXQAC7RsAAvgGYFYG6QABKOVh-FU2BA", "railway_url": None},
    {"id": 18, "telegram_file_id": "BAACAgUAAxkBAAEZuFFpTwmzDcviZar2TPEVXmOvWTrijgACdhkAAv8HgVVd-CLkXBLR2zYE", "railway_url": None},
    {"id": 19, "telegram_file_id": "BAACAgUAAxkBAAEZuHNpTwrHrYml6MDm0szl23Ni2dDq1AACEx4AAt6QuFWtyQYpLl_YfjYE", "railway_url": None},
    {"id": 20, "telegram_file_id": "BAACAgUAAxkBAAEZuH1pTwrkRD7DGdLzupq7KDe7puawYgACaRcAAmYRwVUc1UNZHB_3xDYE", "railway_url": None},
    {"id": 21, "telegram_file_id": "BAACAgUAAxkBAAEZuIFpTwrtSK8OdoEHDAVksm6wtVHfXQACoRsAAglx0VXcKckdztpQLzYE", "railway_url": None},
    {"id": 22, "telegram_file_id": "BAACAgUAAxkBAAEZuIlpTwsCMSY7DauFLdMstnb8-t3pcAACJBgAAuLz4VVK2wuKowP64DYE", "railway_url": None},
    {"id": 23, "telegram_file_id": "BAACAgUAAxkBAAEZuJVpTwsmk0Fut7sfwwcnP2q1tNa30AACuRoAAi2r4FVCS152pN-QWTYE", "railway_url": None},
    {"id": 24, "telegram_file_id": "BAACAgUAAxkBAAEZuJ9pTws8jxskjc7ktY3SpyQdu0tt4gACLRsAAgna8VWA5EHGCIhmfzYE", "railway_url": None},
    {"id": 25, "telegram_file_id": "BAACAgUAAxkBAAEZuKFpTwtAoX8jl98HvaPPRxCW4I0QJwACQB0AAoKFCVZkdXvpTf7wRzYE", "railway_url": None},
    {"id": 26, "telegram_file_id": "BAACAgUAAxkBAAEZuK1pTwtaQatt-u05obxVchXcZIkwWQAC5hoAAvkSEVY6jbPD0WzUwTYE", "railway_url": None},
    {"id": 27, "telegram_file_id": "BAACAgUAAxkBAAEZuLNpTwtpQkwZxGK_Wo7k8EGyKrr-qgAC_hoAAjY6IVa2TjiGsPsLozYE", "railway_url": None},
    {"id": 28, "telegram_file_id": "BAACAgUAAxkBAAEZuLlpTwt3msAGJhBdFJ4lv_iE69pTegAC4xoAAjY6IVbCtvJwQNOkAjYE", "railway_url": None},
    {"id": 29, "telegram_file_id": "BAACAgUAAxkBAAEZuLtpTwt6lL4LCIiwDC7KS-t-cEHP3gAC8BoAAjY6KVaG3sShyZ499zYE", "railway_url": None},
    {"id": 30, "telegram_file_id": "BAACAgUAAxkBAAEZuMFpTwuH1UnVol8sXhFjCOqlm-ULdgACax0AAndcOVateGN1rKtLLDYE", "railway_url": None},
    {"id": 31, "telegram_file_id": "BAACAgUAAxkBAAEZuMVpTwuPErwTF_ijHj32cV2Clo7mcAAC3B8AAkXNSVbsEZO0-_XR7jYE", "railway_url": None},
    {"id": 32, "telegram_file_id": "BAACAgUAAxkBAAEZuM9pTwuiBV1UGuHYH153jNJTNLbq4AACASwAAvgGWFY5epVYCXQ__DYE", "railway_url": None},
    {"id": 33, "telegram_file_id": "AgACAgUAAxkBAAEZuFdpTwpqkUwp1DCoqA2BjpstnicOawACGBFrG9CtiFVfnapgEgrkcQEAAwIAA3kAAzYE", "railway_url": None},
    {"id": 34, "telegram_file_id": "BAACAgUAAxkBAAEZuFtpTwp4LQ7z2LSBfPaueGQXo_OYNQACkBoAAu2DmVUM6sVrShczbzYE", "railway_url": None},
    {"id": 35, "telegram_file_id": "BAACAgUAAxkBAAEZuK9pTwtfyBZdH9kYiejAo0K69md8pgACgxwAAq-7GVYgvPkLXz1CGDYE", "railway_url": None},
    {"id": 36, "telegram_file_id": "BAACAgUAAxkBAAEZuNdpTwuuvAlZykFFNwGYD0EjN_vYWgAC8BsAAvgGYFYgBgux4MCH0TYE", "railway_url": None},
    {"id": 37, "telegram_file_id": "BAACAgUAAxkBAAEZuINpTwryqbudL5VXeuf6RfMQNb007QACpBsAAglx0VVpzho9p9IHgTYE", "railway_url": None},
    {"id": 38, "telegram_file_id": "BAACAgUAAxkBAAEZuJNpTwshr5YDuRyKGRZJOUXn3mbY8QACTBoAAi2r4FULXspRqUHcejYE", "railway_url": None},
    {"id": 39, "telegram_file_id": "BAACAgUAAxkBAAEZuMtpTwuamCe7pumc9FDiLwABFD9MfVUAAuEfAAJFzUlWo3Dght3idNA2BA", "railway_url": None},
    {"id": 40, "telegram_file_id": "BAACAgUAAxkBAAEZuJ1pTws47bsPy5tE9cQxMI7pQt9SYAACPRsAAgna8VUu0EwzwvoSODYE", "railway_url": None},
    {"id": 41, "telegram_file_id": "BAACAgUAAxkBAAEZuGFpTwqNijT6rMIUTkcWZKp7VDk15gACehkAAj_poFX27FmhPcB07TYE", "railway_url": None},
    {"id": 42, "telegram_file_id": "BAACAgUAAxkBAAEZuHdpTwrRmHc-UBxJjAlwgiLWkbmY8AAChhkAApCzwFXm7k4_Y2FlCDYE", "railway_url": None},
    {"id": 43, "telegram_file_id": "BAACAgUAAxkBAAEZuHlpTwrXc1FGxHyOHqtomdt6DLzBdQACiBkAApCzwFXo4X4nSIwlZTYE", "railway_url": None},
    {"id": 44, "telegram_file_id": "BAACAgUAAxkBAAEZuH9pTwrpojJIDT7FHl2iYzqYH__6egACcBcAAmYRwVVX8K59oU-fwDYE", "railway_url": None},
    {"id": 45, "telegram_file_id": "BAACAgUAAxkBAAEZuItpTwsHN9o2iCYIUB9KjaDrCmzTtwACHBgAAuLz4VXCsN67f_zISTYE", "railway_url": None},
    {"id": 46, "telegram_file_id": "BAACAgUAAxkBAAEZuJlpTwsuy4rVQWoKgSsxPzjmtlcnHQACQRsAAgna8VWkGBCnhk204jYE", "railway_url": None},
    {"id": 47, "telegram_file_id": "BAACAgUAAxkBAAEZuKdpTwtN4_BhYMXXVfKcBh86qBO6dgAC8R4AAnWlEFbdKsakajWAaDYE", "railway_url": None},
    {"id": 48, "telegram_file_id": "BAACAgUAAxkBAAEZuMNpTwuLsW4YJ50kIt6Jioi7CWy93AACKRwAAndcOVb8R8qntbgPLTYE", "railway_url": None},
    {"id": 49, "telegram_file_id": "BAACAgUAAxkBAAEZuNFpTwumNcMQzjBLsZIT_fNcytFfGwACBSwAAvgGWFYq4Qf1UaP1UTYE", "railway_url": None},
    {"id": 50, "telegram_file_id": "BAACAgUAAxkBAAEZuI1pTwsM9aCPpARbAsaI3w1u-tV5rAACIRgAAuLz4VW0RbpSwvBrNTYE", "railway_url": None},
    {"id": 51, "telegram_file_id": "BAACAgUAAxkBAAEZuKtpTwtVRjGwlpbK5sZC3w37-A63aQACEh8AAnWlEFbv2kY2EtUfEDYE", "railway_url": None},
    {"id": 52, "telegram_file_id": "BAACAgUAAxkBAAEZuL9pTwuCeEP9lYtabzvp1_P2H1DTHwACLBwAAndcOVbTjL-v5b5O7DYE", "railway_url": None},
    {"id": 53, "telegram_file_id": "BAACAgUAAxkBAAEZuGNpTwqTgpFNxwP2XMnYujb_thDERQACdxkAAj_poFXle9DtbHl4XDYE", "railway_url": None},
    {"id": 54, "telegram_file_id": "BAACAgUAAxkBAAEZuGtpTwqyGxkfFRNC0guZTw8-p_N-mAACgh0AAt6QuFWlj1E0OHQ90TYE", "railway_url": None},
    {"id": 55, "telegram_file_id": "BAACAgUAAxkBAAEZuG1pTwq3z3edB9LFSTkB7DdYoQQKxgACgx0AAt6QuFWf6Cvo91nx8jYE", "railway_url": None},
    {"id": 56, "telegram_file_id": "BAACAgUAAxkBAAEZuG9pTwq8jVtpfzyF88kvrdm44UOBnAACih0AAt6QuFX03j5QT0sckjYE", "railway_url": None},
    {"id": 57, "telegram_file_id": "BAACAgUAAxkBAAEZuHFpTwrBCwuPMQa78VVncFy5bHmUugACix0AAt6QuFXzwcZ0zW9dmTYE", "railway_url": None},
    {"id": 58, "telegram_file_id": "BAACAgUAAxkBAAEZuJtpTwszGZM420MAAaCVCSVVT0EOmn0AAkIbAAIJ2vFV1N3XcAMdGSU2BA", "railway_url": None},
    {"id": 59, "telegram_file_id": "BAACAgUAAxkBAAEZuGVpTwqZn8rLiRNM1FlIapdoWELkvAACfR0AAt6QuFUch0IDoK-nzDYE", "railway_url": None},
    {"id": 60, "telegram_file_id": "BAACAgUAAxkBAAEZuGdpTwqoOrbgyP89zMSSIKKJub_3oAACfh0AAt6QuFV8igHfd0p1YDYE", "railway_url": None},
    {"id": 61, "telegram_file_id": "BAACAgUAAxkBAAEZuGlpTwqtNlrgUlEhdzha6uv_x0pERQACfx0AAt6QuFV3QsbH-vo4VTYE", "railway_url": None},
    {"id": 62, "telegram_file_id": "BAACAgUAAxkBAAEZuI9pTwsRGp6kX_nsulfGJs33P_CRrAACMxgAAuLz4VWSFJ6Tvso49jYE", "railway_url": None},
    {"id": 63, "telegram_file_id": "BAACAgUAAxkBAAEZuJFpTwsaQSr7jh2nNW1FEXTnHSv2rgACNRgAAuLz4VWnKNLyf1HwszYE", "railway_url": None},
    {"id": 64, "telegram_file_id": "BAACAgUAAxkBAAEZuLFpTwtkHUxNGHcjUnYMxO2RBRVjrgACNB8AAsgKEVZPB7hhZjOUOzYE", "railway_url": None},
    {"id": 65, "telegram_file_id": "BAACAgUAAxkBAAEZuKNpTwtEEhX49udlz6vEB8NZgoSrWAACPh4AAnWlCFZ4_n4Kglb-tjYE", "railway_url": None},
    {"id": 66, "telegram_file_id": "BAACAgUAAxkBAAEZuKVpTwtJ2Tk9xXD4UWBTR5egeb6ZnwACNR4AAnWlCFaRGLJ4mzffTjYE", "railway_url": None}
]

@app.on_event("startup")
async def on_startup():
    await client.start()

@app.on_event("shutdown")
async def on_shutdown():
    await client.stop()

@app.get("/")
def health_check():
    return {"status": "active", "lectures_count": len(lectures_db)}

@app.get("/videos")
def get_videos():
    return lectures_db

@app.get("/stream/{lecture_id}")
async def stream_video(lecture_id: int):
    # 1. Find lecture
    lecture = next((l for l in lectures_db if l["id"] == lecture_id), None)
    
    if not lecture:
        raise HTTPException(status_code=404, detail=f"Lecture {lecture_id} not found")

    # 2. Try Telegram Source
    if lecture.get("telegram_file_id"):
        file_id = lecture["telegram_file_id"]
        
        try:
            # We use Pyrogram to stream the file chunks.
            # This proxies the traffic through Railway, bypassing the 20MB Bot API limit.
            
            async def chunk_generator():
                try:
                    # chunk_size is mostly managed by Pyrogram, but we can iterate
                    async for chunk in client.stream_media(file_id):
                        yield chunk
                except Exception as e:
                    print(f"Stream interrupted: {e}")

            return StreamingResponse(chunk_generator(), media_type="video/mp4")

        except Exception as e:
            print(f"Streaming Setup Error: {e}")
            raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")

    # 3. Fallback to Railway URL (if provided)
    if lecture.get("railway_url"):
        return RedirectResponse(lecture["railway_url"])

    # 4. If all fails
    raise HTTPException(status_code=404, detail="Video source unavailable")
