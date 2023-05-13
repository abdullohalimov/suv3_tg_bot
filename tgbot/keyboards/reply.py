from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton

def phone_keyboard():
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text='📱 Рақам юбориш', request_contact=True))
    return keyboard.as_markup(one_time_keyboard=True, resize_keyboard=True)