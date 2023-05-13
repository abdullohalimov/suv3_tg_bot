from aiogram.filters.state import State, StatesGroup

class UserRegistration(StatesGroup):
    phone = State()
    fullname = State()
    birthday = State()
    malefemale = State()
    fermer_xojalik = State()
    position = State()
    address_region = State()
    address_district = State()
    faoliyat_turi = State()
    cert = State()