from aiogram.utils.keyboard import ReplyKeyboardBuilder

def reply_keyboard_convert():
    keyboard = ReplyKeyboardBuilder()

    keyboard.button(text='Конвертация')
    keyboard.button(text='История')

    keyboard.adjust(2)

    return keyboard.as_markup(resize_keyboard=True)