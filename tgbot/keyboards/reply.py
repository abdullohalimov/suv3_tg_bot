from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton
from tgbot.misc.states import i18nn as _

def phone_keyboard(lang):
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text=_('📱 Рақам юбориш', locale=lang), request_contact=True))
    keyboard.add(KeyboardButton(text=_('🔙 Орқага', locale=lang)))
    keyboard.adjust(1)

    return keyboard.as_markup(one_time_keyboard=True, resize_keyboard=True)

def back_keyboard(lang):
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text=_('🔙 Орқага', locale=lang)))
    return keyboard.as_markup(one_time_keyboard=True, resize_keyboard=True)
