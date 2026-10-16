import os

from aiogram import Bot, Dispatcher

from .handlers import get_main_router

TOKEN = os.getenv("TELEGRAM_MASTER_BOT_TOKEN", "-1")

# ========================= BOT =========================


class MainBot:
    def __init__(self) -> None:
        self.bot = Bot(token=TOKEN)
        self.dp = Dispatcher()
        
    # async def handle_image(self, message: Message) -> None:
    #     photo = message.photo[-1]
    #     buf = io.BytesIO()
    #     await self.bot.download(photo.file_id, destination=buf)
    #
    #     try:
    #         url = await upload_photo_api(buf.getvalue(), f"{photo.file_id}.jpg", "image/jpeg")
    #         await message.reply(f"Фото успішно завантажено: {url}")
    #     except RuntimeError as e:
    #         await message.reply(f"Помилка при завантаженні фото: {e}")

    async def run(self) -> None:
        
        self.dp.include_router(get_main_router())
        
        try:
            print("Starting Master Bot...")
            await self.dp.start_polling(self.bot)
        finally:
            await self.bot.session.close()
