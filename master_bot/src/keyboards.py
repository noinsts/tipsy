from typing import Any

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def _short_label(value: object, limit: int = 42) -> str:
    text = str(value or "Без назви")
    return text if len(text) <= limit else text[: limit - 1] + "…"


def get_hub_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👥 Управління працівниками", callback_data="employees")],
        [InlineKeyboardButton(text="☕ Управління закладами", callback_data="cafes")],
    ])


def get_employees_keyboard(employees: list[dict[str, Any]]) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(
            text=f"{'🟢' if employee.get('active') else '⏸️'} {_short_label(employee.get('name'), 42)} · #{employee.get('id')}",
            callback_data=f"employee:view:{employee.get('id')}",
        )]
        for employee in employees
    ]
    rows.append([InlineKeyboardButton(text="➕ Додати працівника", callback_data="employee:add")])
    rows.append([InlineKeyboardButton(text="↩️ Головне меню", callback_data="hub")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_employee_details_keyboard(employee_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✏️ Редагувати", callback_data=f"employee:edit:{employee_id}")],
        [InlineKeyboardButton(text="🗑 Видалити", callback_data=f"employee:delete:{employee_id}")],
        [InlineKeyboardButton(text="⬅️ До працівників", callback_data="employees")],
    ])


def get_employee_fields_keyboard(employee_id: int) -> InlineKeyboardMarkup:
    fields = [
        ("Ім’я", "name"),
        ("Telegram ID", "telegramId"),
        ("Дата народження", "birthdayDate"),
        ("Посилання на банку", "jarUrl"),
        ("Фото", "photoUrl"),
        ("Статус активності", "active"),
    ]
    rows = [
        [InlineKeyboardButton(text=label, callback_data=f"employee:field:{employee_id}:{field}")]
        for label, field in fields
    ]
    rows.append([InlineKeyboardButton(text="⬅️ Назад", callback_data=f"employee:view:{employee_id}")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_confirm_delete_keyboard(entity: str, entity_id: int, back_callback: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Так, видалити", callback_data=f"{entity}:delete-confirm:{entity_id}")],
        [InlineKeyboardButton(text="Ні, залишити", callback_data=back_callback)],
    ])


def get_cafes_keyboard(cafes: list[dict[str, Any]]) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(
            text=f"☕ {_short_label(cafe.get('name'), 42)} · #{cafe.get('id')}",
            callback_data=f"cafe:view:{cafe.get('id')}",
        )]
        for cafe in cafes
    ]
    rows.append([InlineKeyboardButton(text="➕ Додати заклад", callback_data="cafe:add")])
    rows.append([InlineKeyboardButton(text="↩️ Головне меню", callback_data="hub")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_cafe_details_keyboard(cafe_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✏️ Редагувати", callback_data=f"cafe:edit:{cafe_id}")],
        [InlineKeyboardButton(text="🗑 Видалити", callback_data=f"cafe:delete:{cafe_id}")],
        [InlineKeyboardButton(text="⬅️ До закладів", callback_data="cafes")],
    ])


def get_cafe_fields_keyboard(cafe_id: int) -> InlineKeyboardMarkup:
    fields = [
        ("Назва", "name"),
        ("Опис", "description"),
        ("Адреса", "address"),
        ("Тип закладу", "type"),
        ("Фото", "photoUrl"),
        ("Slug / адреса сторінки", "slug"),
    ]
    rows = [
        [InlineKeyboardButton(text=label, callback_data=f"cafe:field:{cafe_id}:{field}")]
        for label, field in fields
    ]
    rows.append([InlineKeyboardButton(text="⬅️ Назад", callback_data=f"cafe:view:{cafe_id}")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_cafe_type_keyboard(action: str, cafe_id: int | None = None) -> InlineKeyboardMarkup:
    if action == "create":
        prefix = "cafe:create-type"
    else:
        prefix = f"cafe:edit-type:{cafe_id}"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Zona", callback_data=f"{prefix}:zona")],
        [InlineKeyboardButton(text="Doner", callback_data=f"{prefix}:doner")],
    ])


def get_active_keyboard(employee_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Активний", callback_data=f"employee:set-active:{employee_id}:true")],
        [InlineKeyboardButton(text="⏸ Неактивний", callback_data=f"employee:set-active:{employee_id}:false")],
    ])
