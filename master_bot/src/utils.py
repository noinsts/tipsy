from aiogram.types import Message, CallbackQuery

async def send_message(event: Message | CallbackQuery, **kwargs) -> None:
    if isinstance(event, CallbackQuery):
        await event.message.edit_text(**kwargs)
    elif isinstance(event, Message):
        await event.answer(**kwargs)
