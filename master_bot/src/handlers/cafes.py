import re

import aiohttp
from aiogram import Bot, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from .base import BaseHandler
from .form_helpers import api_error_text, read_photo_value
from .. import api
from ..keyboards import (
    get_cafe_details_keyboard,
    get_cafe_fields_keyboard,
    get_cafe_type_keyboard,
    get_cafes_keyboard,
    get_confirm_delete_keyboard,
    get_hub_keyboard,
)

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class CafeCreate(StatesGroup):
    name = State()
    description = State()
    address = State()
    type = State()
    photo_url = State()
    slug = State()


class CafeEdit(StatesGroup):
    value = State()


def cafe_details_text(cafe: dict) -> str:
    return (
        f"☕ Заклад #{cafe.get('id')}\n\n"
        f"Назва: {cafe.get('name', '—')}\n"
        f"Опис: {cafe.get('description', '—')}\n"
        f"Адреса: {cafe.get('address', '—')}\n"
        f"Тип: {cafe.get('type', '—')}\n"
        f"Фото: {cafe.get('photoUrl', '—')}\n"
        f"Slug: {cafe.get('slug', '—')}"
    )


def cafe_payload(cafe: dict) -> dict:
    return {
        "name": cafe.get("name"),
        "description": cafe.get("description"),
        "address": cafe.get("address"),
        "type": cafe.get("type"),
        "photoUrl": cafe.get("photoUrl"),
        "slug": cafe.get("slug"),
    }


def validate_slug(value: str) -> str:
    slug = value.strip()
    if not SLUG_RE.fullmatch(slug):
        raise ValueError("Slug має містити лише маленькі латинські літери, цифри й дефіси, наприклад zona-berezan.")
    return slug


class CafeHandler(BaseHandler):
    def register_handler(self) -> None:
        self.router.message.register(self.cancel_form, Command("cancel"))
        self.router.callback_query.register(self.show_cafes, F.data == "cafes")
        self.router.callback_query.register(self.start_create, F.data == "cafe:add")
        self.router.callback_query.register(self.create_type, F.data.startswith("cafe:create-type:"))
        self.router.callback_query.register(self.edit_type, F.data.startswith("cafe:edit-type:"))
        self.router.callback_query.register(self.show_details, F.data.startswith("cafe:view:"))
        self.router.callback_query.register(self.start_edit, F.data.startswith("cafe:edit:"))
        self.router.callback_query.register(self.choose_field, F.data.startswith("cafe:field:"))
        self.router.callback_query.register(self.ask_delete, F.data.startswith("cafe:delete:"))
        self.router.callback_query.register(self.confirm_delete, F.data.startswith("cafe:delete-confirm:"))

        self.router.message.register(self.create_name, CafeCreate.name)
        self.router.message.register(self.create_description, CafeCreate.description)
        self.router.message.register(self.create_address, CafeCreate.address)
        self.router.message.register(self.create_photo_url, CafeCreate.photo_url)
        self.router.message.register(self.create_slug, CafeCreate.slug)
        self.router.message.register(self.edit_value, CafeEdit.value)

    async def show_cafes(self, event: Message | CallbackQuery) -> None:
        try:
            cafes = await api.fetch_all_managed_cafes()
            text = "☕ Заклади\n\nОбери заклад або додай новий." if cafes else (
                "☕ Заклади\n\nСписок поки порожній — можна створити перший заклад."
            )
            markup = get_cafes_keyboard(cafes)
        except (api.ApiError, aiohttp.ClientError, RuntimeError) as exc:
            text, markup = f"⚠️ {api_error_text(exc)}", get_hub_keyboard()
        if isinstance(event, CallbackQuery):
            await event.answer()
            await event.message.edit_text(text, reply_markup=markup)
        else:
            await event.answer(text, reply_markup=markup)

    async def show_details(self, callback: CallbackQuery) -> None:
        await callback.answer()
        cafe_id = int(callback.data.split(":")[2])
        await self._show_details(callback, cafe_id)

    async def _show_details(self, event: Message | CallbackQuery, cafe_id: int) -> None:
        try:
            cafe = await api.fetch_cafe(cafe_id)
            text, markup = cafe_details_text(cafe), get_cafe_details_keyboard(cafe_id)
        except (api.ApiError, aiohttp.ClientError, RuntimeError) as exc:
            text, markup = f"⚠️ {api_error_text(exc)}", get_cafes_keyboard([])
        if isinstance(event, CallbackQuery):
            await event.message.edit_text(text, reply_markup=markup)
        else:
            await event.answer(text, reply_markup=markup)

    async def start_create(self, callback: CallbackQuery, state: FSMContext) -> None:
        await callback.answer()
        await state.clear()
        await state.set_state(CafeCreate.name)
        await callback.message.edit_text("➕ Новий заклад\n\nВведи назву.\nДля скасування: /cancel")

    async def create_name(self, message: Message, state: FSMContext) -> None:
        value = (message.text or "").strip()
        if not value:
            await message.answer("Назва не може бути порожньою.")
            return
        await state.update_data(name=value)
        await state.set_state(CafeCreate.description)
        await message.answer("Введи короткий опис закладу.")

    async def create_description(self, message: Message, state: FSMContext) -> None:
        value = (message.text or "").strip()
        if not value:
            await message.answer("Опис не може бути порожнім.")
            return
        await state.update_data(description=value)
        await state.set_state(CafeCreate.address)
        await message.answer("Введи адресу закладу.")

    async def create_address(self, message: Message, state: FSMContext) -> None:
        value = (message.text or "").strip()
        if not value:
            await message.answer("Адреса не може бути порожньою.")
            return
        await state.update_data(address=value)
        await state.set_state(CafeCreate.type)
        await message.answer("Обери тип закладу:", reply_markup=get_cafe_type_keyboard("create"))

    async def create_type(self, callback: CallbackQuery, state: FSMContext) -> None:
        await callback.answer()
        cafe_type = callback.data.split(":")[-1]
        if cafe_type not in {"zona", "doner"}:
            await callback.message.answer("Невідомий тип закладу. Спробуй ще раз.")
            return
        if await state.get_state() != CafeCreate.type.state:
            await callback.message.answer("Цей крок уже неактивний. Почни створення закладу знову через меню.")
            return
        await state.update_data(type=cafe_type)
        await state.set_state(CafeCreate.photo_url)
        await callback.message.edit_text("Надішли фото закладу файлом або посиланням http(s).")

    async def create_photo_url(self, message: Message, state: FSMContext, bot: Bot) -> None:
        try:
            value = await read_photo_value(message, bot, allow_clear=False)
        except (ValueError, api.ApiError, aiohttp.ClientError, RuntimeError) as exc:
            await message.answer(str(exc) if isinstance(exc, ValueError) else api_error_text(exc))
            return
        await state.update_data(photoUrl=value)
        await state.set_state(CafeCreate.slug)
        await message.answer("Введи slug для адреси сторінки — маленькі латинські літери, цифри й дефіси. Наприклад: zona-berezan.")

    async def create_slug(self, message: Message, state: FSMContext) -> None:
        try:
            slug = validate_slug(message.text or "")
        except ValueError as exc:
            await message.answer(str(exc))
            return
        payload = await state.get_data()
        payload["slug"] = slug
        try:
            cafe = await api.create_cafe(payload)
        except (api.ApiError, aiohttp.ClientError, RuntimeError) as exc:
            await message.answer(
                f"⚠️ Заклад не створено. {api_error_text(exc)}\nВведи slug ще раз або /cancel."
            )
            return
        await state.clear()
        await message.answer(f"✅ Заклад «{cafe.get('name')}» створено.")
        await self.show_cafes(message)

    async def start_edit(self, callback: CallbackQuery, state: FSMContext) -> None:
        await callback.answer()
        await state.clear()
        cafe_id = int(callback.data.split(":")[2])
        try:
            cafe = await api.fetch_cafe(cafe_id)
            await callback.message.edit_text(
                f"✏️ Що редагуємо у закладу «{cafe.get('name')}»?",
                reply_markup=get_cafe_fields_keyboard(cafe_id),
            )
        except (api.ApiError, aiohttp.ClientError, RuntimeError) as exc:
            await callback.message.edit_text(f"⚠️ {api_error_text(exc)}", reply_markup=get_cafes_keyboard([]))

    async def choose_field(self, callback: CallbackQuery, state: FSMContext) -> None:
        await callback.answer()
        _, _, raw_id, field = callback.data.split(":", 3)
        cafe_id = int(raw_id)
        if field == "type":
            await callback.message.edit_text("Обери новий тип закладу:", reply_markup=get_cafe_type_keyboard("edit", cafe_id))
            return
        prompts = {
            "name": "Введи нову назву.",
            "description": "Введи новий опис.",
            "address": "Введи нову адресу.",
            "photoUrl": "Надішли нове фото файлом або посиланням http(s).",
            "slug": "Введи новий slug (маленькі латинські літери, цифри й дефіси).",
        }
        await state.clear()
        await state.update_data(cafe_id=cafe_id, field=field)
        await state.set_state(CafeEdit.value)
        await callback.message.edit_text(f"{prompts.get(field, 'Введи нове значення.')}\n\nДля скасування: /cancel")

    async def edit_type(self, callback: CallbackQuery) -> None:
        await callback.answer()
        _, _, raw_id, cafe_type = callback.data.split(":")
        cafe_id = int(raw_id)
        if cafe_type not in {"zona", "doner"}:
            await callback.message.answer("Невідомий тип закладу.")
            return
        try:
            cafe = await api.fetch_cafe(cafe_id)
            payload = cafe_payload(cafe)
            payload["type"] = cafe_type
            await api.update_cafe(cafe_id, payload)
        except (api.ApiError, aiohttp.ClientError, RuntimeError) as exc:
            await callback.message.edit_text(f"⚠️ Зміни не збережено. {api_error_text(exc)}", reply_markup=get_cafe_fields_keyboard(cafe_id))
            return
        await self._show_details(callback, cafe_id)

    async def edit_value(self, message: Message, state: FSMContext, bot: Bot) -> None:
        data = await state.get_data()
        cafe_id = int(data["cafe_id"])
        field = data["field"]
        try:
            if field == "photoUrl":
                value = await read_photo_value(message, bot, allow_clear=False)
            elif field == "slug":
                value = validate_slug(message.text or "")
            else:
                value = (message.text or "").strip()
                if not value:
                    raise ValueError("Значення не може бути порожнім.")
        except (ValueError, TypeError) as exc:
            await message.answer(str(exc) or "Некоректне значення. Спробуй ще раз.")
            return
        except (api.ApiError, aiohttp.ClientError, RuntimeError) as exc:
            await message.answer(f"⚠️ {api_error_text(exc)}")
            return

        try:
            cafe = await api.fetch_cafe(cafe_id)
            payload = cafe_payload(cafe)
            payload[field] = value
            await api.update_cafe(cafe_id, payload)
        except (api.ApiError, aiohttp.ClientError, RuntimeError) as exc:
            if isinstance(exc, api.ApiError) and exc.status == 404:
                await state.clear()
                await message.answer(f"⚠️ {api_error_text(exc)}")
                await self.show_cafes(message)
            else:
                await message.answer(
                    f"⚠️ Зміни не збережено. {api_error_text(exc)}\n"
                    "Надішли нове значення ще раз або /cancel."
                )
            return

        await state.clear()
        await message.answer("✅ Зміни збережено.")
        await self._show_details(message, cafe_id)

    async def ask_delete(self, callback: CallbackQuery, state: FSMContext) -> None:
        await callback.answer()
        await state.clear()
        cafe_id = int(callback.data.split(":")[2])
        try:
            cafe = await api.fetch_cafe(cafe_id)
            text = f"🗑 Точно видалити заклад «{cafe.get('name')}»? Цю дію не можна скасувати."
        except (api.ApiError, aiohttp.ClientError, RuntimeError) as exc:
            text = f"⚠️ {api_error_text(exc)}"
        await callback.message.edit_text(
            text,
            reply_markup=get_confirm_delete_keyboard("cafe", cafe_id, f"cafe:view:{cafe_id}"),
        )

    async def confirm_delete(self, callback: CallbackQuery, state: FSMContext) -> None:
        await callback.answer()
        cafe_id = int(callback.data.split(":")[2])
        try:
            await api.delete_cafe(cafe_id)
        except (api.ApiError, aiohttp.ClientError, RuntimeError) as exc:
            await callback.message.edit_text(
                f"⚠️ Не вдалося видалити заклад. {api_error_text(exc)}\n\nЯкщо до закладу прив’язані зміни, спочатку розв’яжи цей зв’язок.",
                reply_markup=get_cafe_details_keyboard(cafe_id),
            )
            return
        await callback.message.edit_text("✅ Заклад видалено.")
        await self.show_cafes(callback.message)

    async def cancel_form(self, message: Message, state: FSMContext) -> None:
        await state.clear()
        await message.answer("Введення скасовано.", reply_markup=get_hub_keyboard())
