from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_hub_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Управління працівниками', callback_data='employees')],
        [InlineKeyboardButton(text='Управління закладами', callback_data='cafes')],
    ])
