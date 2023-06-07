from aiogram.filters.state import State, StatesGroup
from aiogram.utils.i18n import I18n

i18n = I18n(path="locales", default_locale="uz", domain="messages")

i18nn = i18n.gettext


class UserRegistration(StatesGroup):
    language = State()
    phone = State()

    full_name = State()
    birthday = State()
    malefemale = State()
    fermer_xojalik = State()
    position = State()
    address_region = State()
    address_district = State()
    faoliyat_turi = State()
    cert = State()
    cert2 = State()

class Survey(StatesGroup):
    test = State()


    
class UserStates(StatesGroup):
    language = State()
    id = State()
    first = State()
    second = State()
    third = State()
    four = State()
    five = State()
    six = State()
    seven = State()