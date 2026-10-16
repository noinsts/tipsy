from datetime import date

import aiohttp
from aiogram import Bot, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from .base import BaseHandler
from .form_helpers import api_error_text, is_http_url, parse_active, read_photo_value
from .. import api
from ..keyboards import (
    get_active_keyboard,
    get_confirm_delete_keyboard,
    get_employee_details_keyboard,
    get_employee_fields_keyboard,
    get_employees_keyboard,
    get_hub_keyboard,
)


class EmployeeCreate(StatesGroup):
    name = State()
    telegram_id = State()
    birthday_date = State()
    jar_url = State()
    photo_url = State()
    active = State()


class EmployeeEdit(StatesGroup):
    value = State()


def employee_details_text(employee: dict) -> str:
    active = "🟢 активний" if employee.get("active") else "⏸ неактивний"
    photo_url = employee.get("photoUrl") or "не задано"
    return (
        f"👤 Працівник #{employee.get('id')}\n\n"
        f"Ім’я: {employee.get('name', '—')}\n"
        f"Telegram ID: {employee.get('telegramId', '—')}\n"
        f"Дата народження: {employee.get('birthdayDate', '—')}\n"
        f"Посилання на банку: {employee.get('jarUrl', '—')}\n"
        f"Фото: {photo_url}\n"
        f"Статус: {active}"
    )


def employee_payload(employee: dict) -> dict:
    return {
        "name": employee.get("name"),
        "telegramId": employee.get("telegramId"),
        "birthdayDate": employee.get("birthdayDate"),
        "jarUrl": employee.get("jarUrl"),
        "photoUrl": employee.get("photoUrl"),
        "active": bool(employee.get("active")),
    }



class EmployeeHandler(BaseHandler):
    def register_handler(self) -> None:
        self.router.message.register(self.cancel_form, Command("cancel"))
        self.router.callback_query.register(self.show_employees, F.data == "employees")
        self.router.callback_query.register(self.start_create, F.data == "employee:add")
        self.router.callback_query.register(self.show_details, F.data.startswith("employee:view:"))
        self.router.callback_query.register(self.start_edit, F.data.startswith("employee:edit:"))
        self.router.callback_query.register(self.choose_field, F.data.startswith("employee:field:"))
        self.router.callback_query.register(self.set_active, F.data.startswith("employee:set-active:"))
        self.router.callback_query.register(self.ask_delete, F.data.startswith("employee:delete:"))
        self.router.callback_query.register(self.confirm_delete, F.data.startswith("employee:delete-confirm:"))

        self.router.message.register(self.create_name, EmployeeCreate.name)
        self.router.message.register(self.create_telegram_id, EmployeeCreate.telegram_id)
        self.router.message.register(self.create_birthday_date, EmployeeCreate.birthday_date)
        self.router.message.register(self.create_jar_url, EmployeeCreate.jar_url)
        self.router.message.register(self.create_photo_url, EmployeeCreate.photo_url)
        self.router.message.register(self.create_active, EmployeeCreate.active)
        self.router.message.register(self.edit_value, EmployeeEdit.value)

    async def show_employees(self, event: Message | CallbackQuery) -> None:
        try:
            employees = await api.fetch_all_employees()
            text = "👥 Працівники\n\nОбери працівника або додай нового." if employees else (
                "👥 Працівники\n\nСписок поки порожній — можна додати першого працівника."
            )
            markup = get_employees_keyboard(employees)
        except (api.ApiError, aiohttp.ClientError, RuntimeError) as exc:
            text, markup = f"⚠️ {api_error_text(exc)}", get_hub_keyboard()
        if isinstance(event, CallbackQuery):
            await event.answer()
            await event.message.edit_text(text, reply_markup=markup)
        else:
            await event.answer(text, reply_markup=markup)

    async def show_details(self, callback: CallbackQuery) -> None:
        await callback.answer()
        employee_id = int(callback.data.split(":")[2])
        await self._show_details(callback, employee_id)

    async def _show_details(self, event: Message | CallbackQuery, employee_id: int) -> None:
        try:
            employee = await api.fetch_employee(employee_id)
            text = employee_details_text(employee)
            markup = get_employee_details_keyboard(employee_id)
        except (api.ApiError, aiohttp.ClientError, RuntimeError) as exc:
            text, markup = f"⚠️ {api_error_text(exc)}", get_employees_keyboard([])
        if isinstance(event, CallbackQuery):
            await event.message.edit_text(text, reply_markup=markup)
        else:
            await event.answer(text, reply_markup=markup)

    async def start_create(self, callback: CallbackQuery, state: FSMContext) -> None:
        await callback.answer()
        await state.clear()
        await state.set_state(EmployeeCreate.name)
        await callback.message.edit_text("➕ Новий працівник\n\nВведи ім’я та прізвище.\nДля скасування: /cancel")

    async def create_name(self, message: Message, state: FSMContext) -> None:
        value = (message.text or "").strip()
        if not value:
            await message.answer("Ім’я не може бути порожнім. Спробуй ще раз.")
            return
        await state.update_data(name=value)
        await state.set_state(EmployeeCreate.telegram_id)
        await message.answer("Введи Telegram ID працівника (число).")

    async def create_telegram_id(self, message: Message, state: FSMContext) -> None:
        try:
            value = int((message.text or "").strip())
            if value <= 0:
                raise ValueError
        except ValueError:
            await message.answer("Telegram ID має бути додатним цілим числом. Спробуй ще раз.")
            return
        await state.update_data(telegramId=value)
        await state.set_state(EmployeeCreate.birthday_date)
        await message.answer("Введи дату народження у форматі РРРР-ММ-ДД, наприклад 2001-04-23.")

    async def create_birthday_date(self, message: Message, state: FSMContext) -> None:
        try:
            value = date.fromisoformat((message.text or "").strip()).isoformat()
        except ValueError:
            await message.answer("Не схоже на дату. Потрібен формат РРРР-ММ-ДД, наприклад 2001-04-23.")
            return
        await state.update_data(birthdayDate=value)
        await state.set_state(EmployeeCreate.jar_url)
        await message.answer("Надішли посилання на банку (http:// або https://).")

    async def create_jar_url(self, message: Message, state: FSMContext) -> None:
        value = (message.text or "").strip()
        if not is_http_url(value):
            await message.answer("Потрібне повне посилання, що починається з http:// або https://.")
            return
        await state.update_data(jarUrl=value)
        await state.set_state(EmployeeCreate.photo_url)
        await message.answer("Надішли фото працівника файлом або посиланням. Надішли '-' якщо фото поки немає.")

    async def create_photo_url(self, message: Message, state: FSMContext, bot: Bot) -> None:
        try:
            value = await read_photo_value(message, bot, allow_clear=True)
        except (ValueError, api.ApiError, aiohttp.ClientError, RuntimeError) as exc:
            await message.answer(str(exc) if isinstance(exc, ValueError) else api_error_text(exc))
            return
        await state.update_data(photoUrl=value)
        await state.set_state(EmployeeCreate.active)
        await message.answer("Працівник активний? Введи \"Так\" або \"Ні\".")

    async def create_active(self, message: Message, state: FSMContext) -> None:
        try:
            active = parse_active(message.text or "")
        except ValueError as exc:
            await message.answer(str(exc))
            return
        payload = await state.get_data()
        payload["active"] = active
        try:
            created = await api.create_employee(payload)
        except (api.ApiError, aiohttp.ClientError, RuntimeError) as exc:
            if isinstance(exc, api.ApiError) and exc.status == 409:
                await state.set_state(EmployeeCreate.telegram_id)
                await message.answer(
                    f"⚠️ Працівника не створено. {api_error_text(exc)}\nВведи інший Telegram ID."
                )
            else:
                await message.answer(
                    f"⚠️ Працівника не створено. {api_error_text(exc)}\n"
                    "Спробуй ще раз: введи \"Так\" або \"ні\", або /cancel."
                )
            return
        await state.clear()
        await message.answer(f"✅ Працівника «{created.get('name')}» створено.")
        await self.show_employees(message)

    async def start_edit(self, callback: CallbackQuery, state: FSMContext) -> None:
        await callback.answer()
        await state.clear()
        employee_id = int(callback.data.split(":")[2])
        try:
            employee = await api.fetch_employee(employee_id)
            text = f"✏️ Що редагуємо у працівника «{employee.get('name')}»?"
            await callback.message.edit_text(text, reply_markup=get_employee_fields_keyboard(employee_id))
        except (api.ApiError, aiohttp.ClientError, RuntimeError) as exc:
            await callback.message.edit_text(f"⚠️ {api_error_text(exc)}", reply_markup=get_employees_keyboard([]))

    async def choose_field(self, callback: CallbackQuery, state: FSMContext) -> None:
        await callback.answer()
        _, _, raw_id, field = callback.data.split(":", 3)
        employee_id = int(raw_id)
        if field == "active":
            await callback.message.edit_text(
                "Обери новий статус працівника:",
                reply_markup=get_active_keyboard(employee_id),
            )
            return
        prompts = {
            "name": "Введи нове ім’я та прізвище.",
            "telegramId": "Введи новий Telegram ID (додатне ціле число).",
            "birthdayDate": "Введи нову дату у форматі РРРР-ММ-ДД.",
            "jarUrl": "Введи нове посилання на банку (http:// або https://).",
            "photoUrl": "Надішли нове фото файлом або посиланням. Введи '-' щоб прибрати фото.",
        }
        await state.clear()
        await state.update_data(employee_id=employee_id, field=field)
        await state.set_state(EmployeeEdit.value)
        await callback.message.edit_text(f"{prompts.get(field, 'Введи нове значення.')}\n\nДля скасування: /cancel")

    async def edit_value(self, message: Message, state: FSMContext, bot: Bot) -> None:
        data = await state.get_data()
        employee_id = int(data["employee_id"])
        field = data["field"]
        try:
            if field == "name":
                value = (message.text or "").strip()
                if not value:
                    raise ValueError("Ім’я не може бути порожнім.")
            elif field == "telegramId":
                value = int((message.text or "").strip())
                if value <= 0:
                    raise ValueError("Telegram ID має бути додатним числом.")
            elif field == "birthdayDate":
                value = date.fromisoformat((message.text or "").strip()).isoformat()
            elif field == "jarUrl":
                value = (message.text or "").strip()
                if not is_http_url(value):
                    raise ValueError("Потрібне посилання http:// або https://.")
            elif field == "photoUrl":
                value = await read_photo_value(message, bot, allow_clear=True)
            else:
                raise ValueError("Невідоме поле для редагування.")
        except (ValueError, TypeError) as exc:
            await message.answer(str(exc) or "Некоректне значення. Спробуй ще раз.")
            return
        except (api.ApiError, aiohttp.ClientError, RuntimeError) as exc:
            await message.answer(f"⚠️ {api_error_text(exc)}")
            return

        try:
            employee = await api.fetch_employee(employee_id)
            payload = employee_payload(employee)
            payload[field] = value
            await api.update_employee(employee_id, payload)
        except (api.ApiError, aiohttp.ClientError, RuntimeError) as exc:
            if isinstance(exc, api.ApiError) and exc.status == 404:
                await state.clear()
                await message.answer(f"⚠️ {api_error_text(exc)}")
                await self.show_employees(message)
            else:
                await message.answer(
                    f"⚠️ Зміни не збережено. {api_error_text(exc)}\n"
                    "Надішли нове значення ще раз або /cancel."
                )
            return

        await state.clear()
        await message.answer("✅ Зміни збережено.")
        await self._show_details(message, employee_id)

    async def set_active(self, callback: CallbackQuery, state: FSMContext) -> None:
        await callback.answer()
        _, _, raw_id, raw_value = callback.data.split(":")
        employee_id = int(raw_id)
        active = raw_value == "true"
        try:
            employee = await api.fetch_employee(employee_id)
            payload = employee_payload(employee)
            payload["active"] = active
            await api.update_employee(employee_id, payload)
            await self._show_details(callback, employee_id)
        except (api.ApiError, aiohttp.ClientError, RuntimeError) as exc:
            await callback.message.edit_text(f"⚠️ {api_error_text(exc)}", reply_markup=get_employee_details_keyboard(employee_id))

    async def ask_delete(self, callback: CallbackQuery, state: FSMContext) -> None:
        await callback.answer()
        await state.clear()
        employee_id = int(callback.data.split(":")[2])
        try:
            employee = await api.fetch_employee(employee_id)
            text = f"🗑 Точно видалити працівника «{employee.get('name')}»? Цю дію не можна скасувати."
        except (api.ApiError, aiohttp.ClientError, RuntimeError) as exc:
            text = f"⚠️ {api_error_text(exc)}"
        await callback.message.edit_text(
            text,
            reply_markup=get_confirm_delete_keyboard("employee", employee_id, f"employee:view:{employee_id}"),
        )

    async def confirm_delete(self, callback: CallbackQuery, state: FSMContext) -> None:
        await callback.answer()
        employee_id = int(callback.data.split(":")[2])
        try:
            await api.delete_employee(employee_id)
        except (api.ApiError, aiohttp.ClientError, RuntimeError) as exc:
            await callback.message.edit_text(
                f"⚠️ Не вдалося видалити працівника. {api_error_text(exc)}\n\nЯкщо до працівника прив’язані зміни, спочатку розв’яжи цей зв’язок.",
                reply_markup=get_employee_details_keyboard(employee_id),
            )
            return
        await callback.message.edit_text("✅ Працівника видалено.")
        await self.show_employees(callback.message)

    async def cancel_form(self, message: Message, state: FSMContext) -> None:
        await state.clear()
        await message.answer("Введення скасовано.", reply_markup=get_hub_keyboard())
