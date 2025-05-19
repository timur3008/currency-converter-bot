from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.inline import get_all_currencies, get_convertations_kb

router = Router()

@router.message(F.text == 'Конвертация')
async def handle_convertor(message: Message, state: FSMContext):
    await message.answer(
        text='<b>Выберите валюты, которую хотите сконвертировать</b>',
        reply_markup=get_all_currencies(),
        parse_mode='HTML'
    )
    await state.update_data(convert_from=True)


@router.message(F.text == 'История')
async def handle_history(message: Message):
    await message.answer(
        text='Вот ваша история конвертаций'
    )

    data, convertations_kb = get_convertations_kb(chat_id=message.from_user.id)
    _, from_symbol, to_symbol, number, converted_number, from_code, to_code, time, user_id = data

    await message.answer(
        text=f'<b>DATE: {time[:19]}</b>\n\n<b>{number} {from_code} = {converted_number:.4f} {to_code}</b>\n<b>{number} {from_symbol} = {converted_number:.4f} {to_symbol}</b>',
        reply_markup=convertations_kb,
        parse_mode='HTML'
    )