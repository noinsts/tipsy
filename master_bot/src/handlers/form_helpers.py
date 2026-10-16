from io import BytesIO
from urllib.parse import urlparse

from aiogram import Bot
from aiogram.types import Message

from .. import api
from ..api import upload_photo_api


def api_error_text(exc: Exception) -> str:
    if isinstance(exc, api.ApiError):
        if exc.status == 409:
            return f"Конфлікт даних: {exc.message}."
        if exc.status == 404:
            return "Запис не знайдено. Можливо, його вже видалили."
        if exc.status == 401:
            return "Бекенд відхилив внутрішній токен. Перевір BOT_INTERNAL_TOKEN."
        if exc.status == 400:
            return f"Бекенд відхилив дані: {exc.message}."
        return f"Помилка бекенду ({exc.status}): {exc.message}"
    detail = str(exc)
    if "BOT_INTERNAL_TOKEN" in detail:
        return "Не задано BOT_INTERNAL_TOKEN."
    if "BACKEND_URL" in detail:
        return "Не задано BACKEND_URL."
    if "некоректну JSON" in detail:
        return detail
    return "Не вдалося з’єднатися з бекендом. Перевір BACKEND_URL і чи запущений backend."


def is_http_url(value: str) -> bool:
    try:
        parsed = urlparse(value.strip())
    except ValueError:
        return False
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


async def read_photo_value(message: Message, bot: Bot, *, allow_clear: bool) -> str | None:
    """Accept a Telegram photo, a public URL, or '-' when clearing is allowed."""
    if message.photo:
        photo = message.photo[-1]
        buffer = BytesIO()
        await bot.download(photo.file_id, destination=buffer)
        return await upload_photo_api(buffer.getvalue(), f"telegram-{photo.file_unique_id}.jpg", "image/jpeg")

    value = (message.text or "").strip()
    if allow_clear and value == "-":
        return None
    if not is_http_url(value):
        if allow_clear:
            raise ValueError("Надішли фото файлом, посилання http(s) або '-' щоб очистити поле.")
        raise ValueError("Надішли фото файлом або публічне посилання, що починається з http:// чи https://.")
    return value


def parse_active(value: str) -> bool:
    normalized = value.strip().casefold()
    if normalized in {"так", "т", "yes", "y", "true", "1", "активний", "активна"}:
        return True
    if normalized in {"ні", "н", "no", "n", "false", "0", "неактивний", "неактивна"}:
        return False
    raise ValueError("Введи «так» або «ні».")
