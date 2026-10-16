from aiogram import F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from .base import BaseHandler
from ..utils import send_message
from ..keyboards import get_hub_keyboard

class CommonHandler(BaseHandler):
    def register_handler(self) -> None:
        self.router.callback_query.register(self.hub_handler, F.data == 'hub')
        self.router.message.register(self.hub_handler, CommandStart())

    async def hub_handler(self, event: Message | CallbackQuery) -> None:
        msg = (
            "Привіт!"
        )
        await send_message(event, text=msg, reply_markup=get_hub_keyboard())
