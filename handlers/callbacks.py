import os, requests
from dotenv import load_dotenv
from datetime import datetime

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from keyboards.inline import get_all_currencies, get_convertations_kb
from keyboards.reply import reply_keyboard_convert
from misc.states import Convertor
from database.database import add_convertation

router = Router()

@router.callback_query(F.data.startswith('next_page'))
async def next_currencies(call: CallbackQuery, state: FSMContext):
    _, start, limit, page, total_pages = call.data.split(':')
    state_data = await state.get_data()

    if int(page) == int(total_pages):
        return await call.answer(text='Последняя страница', show_alert=True)

    await call.message.edit_reply_markup(
        reply_markup=get_all_currencies(
            start=int(start) + 4,
            limit=int(limit) + 4,
            current_page=int(page) + 1,
            convert_from=state_data.get('convert_from')
        )
    )

@router.callback_query(F.data.startswith('prev_page'))
async def prev_currencies(call: CallbackQuery, state: FSMContext):
    _, start, limit, page = call.data.split(':')
    state_data = await state.get_data()
    
    if int(page) == 1:
        return await call.answer(text='Первая страница', show_alert=True)
    
    await call.message.edit_reply_markup(
        reply_markup=get_all_currencies(
            start=int(start) - 4,
            limit=int(limit) - 4,
            current_page=int(page) - 1,
            convert_from=state_data.get('convert_from')
        )
    )

@router.callback_query(F.data.startswith('convert_from'))
async def convert_from(call: CallbackQuery, state: FSMContext):
    _, currency_code, currency_symbol = call.data.split(':')

    await call.message.edit_text(
        text='<b>Выберите валюту, на которую хотите перевести</b>',
        reply_markup=get_all_currencies(convert_from=False),
        parse_mode='HTML'
    )
    await state.update_data(convert_from=False, from_currency=f'{currency_code}:{currency_symbol}')

@router.callback_query(F.data.startswith('convert_to'))
async def convert_to(call: CallbackQuery, state: FSMContext):
    _, currency_code, currency_symbol = call.data.split(':')

    await call.message.answer(
        text='<b>Напишите сумму для перевода\nПример: 12 или 13.5</b>',
        reply_markup=None,
        parse_mode='HTML'
    )
    await state.update_data(to_currency=f'{currency_code}:{currency_symbol}')
    await state.set_state(Convertor.text)

@router.message(Convertor.text)
async def convert(message: Message, state: FSMContext):
    state_date = await state.get_data()

    from_currency_code, from_currency_symbol = state_date.get('from_currency').split(':')
    to_currency_code, to_currency_symbol = state_date.get('to_currency').split(':')
    text = message.text

    try:
        number = int(text)
    except Exception as ex:
        return await message.answer(
            text='<b>Число введено неправильно\nВведите число заново</b>',
            parse_mode='HTML'
        )

    data = convert_currency(amount=number, from_currency=from_currency_code, to_currency=to_currency_code)
    converted_number = data[to_currency_code] * number
    await message.answer(
        text=f'<b>{number} {from_currency_code} = {converted_number:.4f} {to_currency_code}</b>\n<b>{number} {from_currency_symbol} = {converted_number:.4f} {to_currency_symbol}</b>',
        reply_markup=reply_keyboard_convert(),
        parse_mode='HTML'
    )

    add_convertation(
        currency_from=from_currency_code,
        currency_to=to_currency_code,
        original_num=float(text),
        converted_num=converted_number,
        from_symbol=from_currency_symbol,
        to_symbol=to_currency_symbol,
        converted_at=datetime.now(),
        chat_id=message.from_user.id
    )
    await state.clear()

def convert_currency(amount: int, from_currency: str, to_currency: str):
    load_dotenv()
    # client = freecurrencyapi.Client(api_key=os.getenv('FREE_CURRENCY_API_KEY'))
    # print(client.status())

    response = requests.get(
        url='https://api.freecurrencyapi.com/v1/latest',
        params={
            'apikey': os.getenv('FREE_CURRENCY_API_KEY'),
            'base_currency': from_currency,
            'currencies': to_currency
        }
    )
    return response.json()['data']

@router.callback_query(F.data.startswith('prev_convertion'))
async def get_prev_convertions(call: CallbackQuery):
    data = call.data.split(':')
    _, index, page, chat_id = data

    if int(page) == 1:
        return await call.answer(
            text='Первая страница',
            show_alert=True
        )
    
    currency_data, currency_kb = get_convertations_kb(
        index=int(index) - 1,
        current_page=int(page) - 1,
        chat_id=chat_id
    )
    _, from_symbol, to_symbol, number, converted_number, from_code, to_code, time, _ = currency_data
    
    await call.message.edit_text(
        text=f'<b>DATE: {time[:19]}</b>\n\n<b>{number} {from_code} = {converted_number:.4f} {to_code}</b>\n<b>{number} {from_symbol} = {converted_number:.4f} {to_symbol}</b>',
        parse_mode='HTML'
    )
    await call.message.edit_reply_markup(
        reply_markup=currency_kb
    )

@router.callback_query(F.data.startswith('next_convertion'))
async def get_next_convertions(call: CallbackQuery):
    _, index, page, total_pages, chat_id = call.data.split(':')
    
    if int(page) == int(total_pages):
        return await call.answer(
            text='Последняя страница',
            show_alert=True
        )
    
    currency_data, currency_kb = get_convertations_kb(
        index=int(index) + 1,
        current_page=int(page) + 1,
        chat_id=chat_id
    )
    _, from_symbol, to_symbol, number, converted_number, from_code, to_code, time, _ = currency_data

    await call.message.edit_text(
        text=f'<b>DATE: {time[:19]}</b>\n\n<b>{number} {from_code} = {converted_number:.4f} {to_code}</b>\n<b>{number} {from_symbol} = {converted_number:.4f} {to_symbol}</b>',
        parse_mode='HTML'
    )
    await call.message.edit_reply_markup(
        reply_markup=currency_kb
    )