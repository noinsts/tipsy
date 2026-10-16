import os
from typing import Any, Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message


class AccessMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable,
        event: Message | CallbackQuery,
        data: dict[str, Any],
    ) -> Any:
        user_id = str(event.from_user.id)
        allowed_users = {
            item.strip()
            for item in os.getenv("ALLOWED_USERS", "").split(",")
            if item.strip()
        }

        if user_id not in allowed_users:
            await event.answer("Доступ заблоковано")
            return None

        return await handler(event, data)
