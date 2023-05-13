from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

def male_female_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Erkak", callback_data=Factories.MaleFemale(id='male').pack()))
    keyboard.add(InlineKeyboardButton(text="Ayol", callback_data=Factories.MaleFemale(id='female').pack()))
    return keyboard.as_markup()

async def position_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="хўжалик рахбари", callback_data=Factories.Position(id=1).pack()))
    keyboard.add(InlineKeyboardButton(text="бухгалтери", callback_data=Factories.Position(id=2).pack()))
    keyboard.add(InlineKeyboardButton(text="ишчиси", callback_data=Factories.Position(id=3).pack()))
    keyboard.adjust(1)
    return keyboard.as_markup()
    
async def regions_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Region 1", callback_data=Factories.Region(id=1).pack()))
    keyboard.add(InlineKeyboardButton(text="Region 2", callback_data=Factories.Region(id=2).pack()))
    keyboard.add(InlineKeyboardButton(text="Region 3", callback_data=Factories.Region(id=3).pack()))
    keyboard.add(InlineKeyboardButton(text="Region 4", callback_data=Factories.Region(id=4).pack()))
    keyboard.add(InlineKeyboardButton(text="Region 5", callback_data=Factories.Region(id=5).pack()))
    keyboard.adjust(2)
    return keyboard.as_markup()

async def district_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="District 1", callback_data=Factories.District(id=1).pack()))
    keyboard.add(InlineKeyboardButton(text="District 2", callback_data=Factories.District(id=2).pack()))
    keyboard.add(InlineKeyboardButton(text="District 3", callback_data=Factories.District(id=3).pack()))
    keyboard.add(InlineKeyboardButton(text="District 4", callback_data=Factories.District(id=4).pack()))
    keyboard.add(InlineKeyboardButton(text="District 5", callback_data=Factories.District(id=5).pack()))
    keyboard.add(InlineKeyboardButton(text="District 6", callback_data=Factories.District(id=6).pack()))
    keyboard.add(InlineKeyboardButton(text="District 7", callback_data=Factories.District(id=7).pack()))
    keyboard.adjust(2)
    return keyboard.as_markup()

async def faoliyat_turi_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Пахтачилик/ғаллачилик", callback_data=Factories.FaoliyatTuri(id=1).pack()))
    keyboard.add(InlineKeyboardButton(text="Боғдорчилик/узумчилик", callback_data=Factories.FaoliyatTuri(id=2).pack()))
    keyboard.add(InlineKeyboardButton(text="Сабзавот-полиз", callback_data=Factories.FaoliyatTuri(id=3).pack()))
    keyboard.add(InlineKeyboardButton(text="Сабзавот-ғалла", callback_data=Factories.FaoliyatTuri(id=1).pack()))
    keyboard.add(InlineKeyboardButton(text="Бошқа йўналиш", callback_data=Factories.FaoliyatTuri(id=1).pack()))
    keyboard.adjust(1)
    return keyboard.as_markup()

async def download_cert():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Сертификатни юклаб олиш", callback_data=Factories.Certificate(id='download').pack()))
    keyboard.adjust(1)

    return keyboard.as_markup()

class Factories:
    class MaleFemale(CallbackData, prefix="male_female"):
        id: str

    class Position(CallbackData, prefix="position"):
        id: str

    class Region(CallbackData, prefix="region"):
        id: str

    class District(CallbackData, prefix="district"):
        id: str

    class FaoliyatTuri(CallbackData, prefix="faoliyat_turi"):
        id: str
    
    class Certificate(CallbackData, prefix="faoliyat_turi"):
        id: str