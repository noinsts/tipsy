from typing import Any, Callable, Dict
import os

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery


class AccessMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable,
            event: Message | CallbackQuery,
            data: Dict[str, Any],
    ) -> Any:
        user_id = str(event.from_user.id)
        ALLOWED_USERS = set(list(os.getenv('ALLOWED_USERS', '').split(',')))

        if user_id not in ALLOWED_USERS:
            await event.answer("Доступ заблоковано")
            return None

        return await handler(event, data)
