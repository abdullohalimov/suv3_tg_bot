from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
import tgbot.misc.states as states
import tgbot.services.api as api

user_router = Router()


@user_router.message(CommandStart())
async def user_start(message: Message):
    await message.reply("Assalomu alaykum!\nBu bot boshlanishi xabari")
    await message.answer(text="Телефон рақамингиз")


@user_router.message(states.UserRegistration.phone)
async def user_phone(message: Message, state: FSMContext):
    if message.text.isdigit():
        if api.check_phone(phone=message.text):
            await state.update_data(phone=message.text)
            await message.answer(text="Ism-sharifingizni kiriting: Umarov Azizbek Ibrohim(ovich) o'g'li")
            await state.set_state(states.UserRegistration.fullname)
        else:
            await message.answer(text="Кечирасиз, бу телефон рақамдан аввал рўйхатдан ўтилган")
    else:
        await message.answer(text="Telefon raqamingiz noto'g'ri, qayta kiriting")

@user_router.message(states.UserRegistration.fullname)
async def user_fullname(message: Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    await message.answer(text="Туғилган санангиз")
    await state.set_state(states.UserRegistration.birthday)

@user_router.message(states.UserRegistration.birthday)
async def user_birthday(message: Message, state: FSMContext):
    await state.update_data(birthday=message.text)
    await message.answer(text="Жинсингиз:")
    await state.set_state(states.UserRegistration.malefemale)

@user_router.callback_query()
async def user_malefemale(call: CallbackQuery, state: FSMContext):
    await state.update_data(malefemale=call.data)
    await call.message.edit_text(text="Фермер ёки деҳқон хўжалиги номи")
    await state.set_state(states.UserRegistration.fermer_xojalik)

@user_router.message(states.UserRegistration.fermer_xojalik)
async def user_fermer_xojalik(message: Message, state: FSMContext):
    await state.update_data(fermer_xojalik=message.text)
    await message.answer(text="Сизнинг лавозимингиз")