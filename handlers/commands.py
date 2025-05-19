from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import CommandStart

from keyboards.reply import reply_keyboard_convert
from database.database import get_user_from_database, add_user_to_database

router = Router()

@router.message(CommandStart())
async def handle_convertor(message: Message):
    print(get_user_from_database(chat_id=message.from_user.id))
    if get_user_from_database(chat_id=message.from_user.id) is None:
        add_user_to_database(chat_id=message.from_user.id)
    await message.answer(
        text='<b>Вас приветствует бот-валютчик\nВыберите действия ниже</b>',
        parse_mode='HTML',
        reply_markup=reply_keyboard_convert()
    )