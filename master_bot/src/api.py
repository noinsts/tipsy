import os

import aiohttp

BACKEND_URL = os.getenv("BACKEND_URL", "-1")
BOT_INTERNAL_TOKEN = os.getenv("BOT_INTERNAL_TOKEN", "-1")

async def fetch_all_cafes():
    url = f"https://{BACKEND_URL}/api/v1/public/cafes"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            body = await resp.json(content_type=None)
            if resp.status != 200:
                raise RuntimeError(f"Failed to fetch all cafes: {resp.status}")
            return body


async def upload_photo_api(data: bytes, filename: str, content_type: str) -> str:
    url = f"http://{BACKEND_URL}/api/v1/bot/images/"
    headers = {
        "X-Bot-Token": BOT_INTERNAL_TOKEN
    }

    form = aiohttp.FormData()
    form.add_field('file', data, filename=filename, content_type=content_type)

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=form, headers=headers) as resp:
            body = await resp.json(content_type=None)
            if resp.status != 200:
                raise RuntimeError(f"Failed to upload photo: {resp.status}")
            return body.get("url", "N/A")