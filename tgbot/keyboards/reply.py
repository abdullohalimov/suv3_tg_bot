from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton
from tgbot.misc.states import i18nn as _

def phone_keyboard():
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text=_('📱 Рақам юбориш'), request_contact=True))
    return keyboard.as_markup(one_time_keyboard=True, resize_keyboard=True)