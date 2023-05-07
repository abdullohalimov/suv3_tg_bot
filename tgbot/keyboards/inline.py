from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton()

def male_female_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Erkak", callback_data="male"))
    keyboard.add(InlineKeyboardButton(text="Ayol", callback_data="female"))
    return keyboard.as_markup()

def lavozim_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="хўжалик рахбари", callback_data="1"))
    keyboard.add(InlineKeyboardButton(text="бухгалтери", callback_data="2"))
    keyboard.add(InlineKeyboardButton(text="ишчиси", callback_data="3"))
    return keyboard.as_markup()
    