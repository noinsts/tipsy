import os
import io

from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message

import asyncio
import aiohttp

TOKEN = os.getenv("TELEGRAM_MASTER_BOT_TOKEN", "-1")
BACKEND_URL = os.getenv("BACKEND_URL", "-1")
BOT_INTERNAL_TOKEN = os.getenv("BOT_INTERNAL_TOKEN", "-1")


# ========================= API =========================


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


# ========================= BOT =========================


class MainBot:
    def __init__(self) -> None:
        self.bot = Bot(token=TOKEN)
        self.dp = Dispatcher()
        
    async def handle_image(self, message: Message) -> None:
        photo = message.photo[-1]
        buf = io.BytesIO()
        await self.bot.download(photo.file_id, destination=buf)
        
        try:
            url = await upload_photo_api(buf.getvalue(), f"{photo.file_id}.jpg", "image/jpeg")
            await message.reply(f"Фото успішно завантажено: {url}")
        except RuntimeError as e:
            await message.reply(f"Помилка при завантаженні фото: {e}")

    async def run(self) -> None:
        router = Router()
        
        router.message.register(self.handle_image, F.photo)
        
        self.dp.include_router(router)
        
        try:
            print("Starting Master Bot...")
            await self.dp.start_polling(self.bot)
        finally:
            await self.bot.session.close()
    
    
if __name__ == "__main__":
    bot = MainBot()
    asyncio.run(bot.run())
