import os

import aiohttp
import asyncio

from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.filters.callback_data import CallbackData

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "-1")
BACKEND_URL = os.getenv("BACKEND_URL", "-1")
BOT_INTERNAL_TOKEN = os.getenv("BOT_INTERNAL_TOKEN", "-1")

# ========================= FILTERS =========================

class CafeFilter(CallbackData, prefix="cafe"):
    id: int

class CloseFilter(CallbackData, prefix="close"):
    id: int

# ======================== KEYBOARDS ========================

def get_open_shift_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text='Заступити на зміну', callback_data='open_shift')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def cafes_list(cafes) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text=cafe.get("name", "Failed"), callback_data=CafeFilter(id=cafe.get("id", -1)).pack())]
        for cafe in cafes]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def close_shift_keyboard(shift_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Закрити', callback_data=CloseFilter(id=shift_id).pack())],
    ])

# ========================= API =========================

async def fetch_cafes():
    url = f"http://{BACKEND_URL}/api/v1/public/cafes"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            return data

async def fetch_barista_by_id(id: int):
    headers = {
        "X-Bot-Token": BOT_INTERNAL_TOKEN
    }
    url = f"http://{BACKEND_URL}/api/v1/bot/barista/{id}"
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data
            return None

async def open_shift(cafe_id: int, employeer_id: int) -> int | None:
    headers = {
        "X-Bot-Token": BOT_INTERNAL_TOKEN
    }
    url = f"http://{BACKEND_URL}/api/v1/bot/shift/open?cafeId={cafe_id}&employeeId={employeer_id}"
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                return int(data)
            return None

async def close_shift(shift_id: int) -> bool:
    headers = {
        "X-Bot-Token": BOT_INTERNAL_TOKEN
    }
    url = f"http://{BACKEND_URL}/api/v1/bot/shift/{shift_id}"
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.delete(url) as resp:
            return resp.status in (200, 204)

# ========================= BOT =========================


class MainBot:
    def __init__(self):
        self.bot = Bot(token=TOKEN)
        self.dp = Dispatcher()

    async def handler(self, message: Message) -> None:
        data = await fetch_barista_by_id(message.from_user.id)

        if not data:
            await message.reply("Ви не бариста. Якщо сталась помилка - виконайте команду /start")
            return

        await message.answer(
            f"Привіт, {data.get('name', 'бариста')}",
            reply_markup=get_open_shift_keyboard(),
        )

    async def show_cafes_list(self, callback: CallbackQuery) -> None:
        await callback.message.edit_text(
            "Обери заклад",
            reply_markup=cafes_list(cafes=await fetch_cafes()),
        )

    async def open_shift(self, callback: CallbackQuery, callback_data: CafeFilter) -> None:
        data = await fetch_barista_by_id(callback.from_user.id)

        if not data:
            await callback.answer("Ти не бариста")
            return

        shift_id = await open_shift(callback_data.id, data.get("id", -1))

        if not shift_id:
            await callback.answer("Неможливо відкрити зміну у цьому закладі")
            return

        await callback.message.edit_text(
            "Зміну відкрито",
            reply_markup=close_shift_keyboard(shift_id=shift_id),
        )

    async def close_shift(self, callback: CallbackQuery, callback_data: CloseFilter) -> None:
        data = await fetch_barista_by_id(callback.from_user.id)

        if not data:
            await callback.answer("Ти не бариста")
            return

        ans = await close_shift(callback_data.id)

        if not ans:
            await callback.answer("Сталась помилка, зміна не закрита")

        await callback.message.edit_text(
            "Зміна успішно закрита",
            reply_markup=get_open_shift_keyboard(),
        )


    async def run(self) -> None:
        router = Router()

        router.message.register(self.handler, CommandStart())
        router.callback_query.register(self.show_cafes_list, F.data == 'open_shift')
        router.callback_query.register(self.open_shift, CafeFilter.filter())
        router.callback_query.register(self.close_shift, CloseFilter.filter())

        self.dp.include_router(router)

        try:
            print("Bot was started!")
            await self.dp.start_polling(self.bot)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    bot = MainBot()
    asyncio.run(bot.run())
