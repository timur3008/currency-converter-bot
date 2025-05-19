import os, requests, json
from googletrans import Translator
from typing import Any

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database.database import get_convertations, get_user_from_database

translator = Translator()

def get_all_currencies(start: int = 0, limit: int = 4, current_page: int = 1, convert_from: bool = True):
    keyboard = InlineKeyboardBuilder()

    # API_KEY = os.getenv('FREE_CURRENCY_API_KEY')
    # url = f'https://api.freecurrencyapi.com/v1/currencies?apikey={API_KEY}'
    # data = requests.get(url=url).json()['data']
    # with open('currencies.json', mode='w', encoding='utf-8') as file:
    #     json.dump(data, file, ensure_ascii=False, indent=4)
    
    with open('currencies.json', mode='r', encoding='utf-8') as file:
        data = json.load(file)

    total_pages = round(len(data) / 4)

    for currency in list(data.values())[start:limit]:
        currency_code = currency['code']
        # currency_name = translator.translate(currency['name'], dest='ru', src='en').text
        currency_name = currency['name']
        currency_symbol = currency['symbol_native']
        if convert_from:
            callback_data = f'convert_from:{currency_code}:{currency_symbol}'
        else:
            callback_data = f'convert_to:{currency_code}:{currency_symbol}'
        keyboard.button(text=currency_name, callback_data=callback_data)
    
    keyboard.adjust(1)

    keyboard.row(
        InlineKeyboardButton(text='<<<', callback_data=f'prev_page:{start}:{limit}:{current_page}'),
        InlineKeyboardButton(text=f'{current_page}/{total_pages}', callback_data='current'),
        InlineKeyboardButton(text='>>>', callback_data=f'next_page:{start}:{limit}:{current_page}:{total_pages}')
    )
    keyboard.row(InlineKeyboardButton(text='На главную', callback_data='home'))

    return keyboard.as_markup()

def get_convertations_kb(index: int = 0, current_page: int = 1, chat_id: int = None) -> tuple[Any, InlineKeyboardMarkup]:
    keyboard = InlineKeyboardBuilder()

    total_pages = len(get_convertations(chat_id=chat_id))
    data = get_convertations(chat_id=chat_id)[index]

    keyboard.row(
        InlineKeyboardButton(text='<<<', callback_data=f'prev_convertion:{index}:{current_page}:{chat_id}'),
        InlineKeyboardButton(text=f'{current_page}:{total_pages}', callback_data='current'),
        InlineKeyboardButton(text='>>>', callback_data=f'next_convertion:{index}:{current_page}:{total_pages}:{chat_id}')
    )

    return data, keyboard.as_markup()
