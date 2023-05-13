import logging
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
import tgbot.misc.states as states
import tgbot.services.api as api
import tgbot.keyboards.inline as inline
import tgbot.keyboards.reply as reply

user_router = Router()


class StepOne:
    @user_router.message(CommandStart())
    async def user_start(message: Message, state: FSMContext):
        data = await state.get_data()
        if data.get("id_number"):
            await message.answer(
                text="✅Сиз муваффақиятли рўйхатдан ўтгансиз.\n🆔Сизнинг <b>ID рақамингиз</b> 202300001.\n\n🎫Курс якунлангандан сўнг, шу ерда <b>сертификатингизни</b> юклаб олишингиз мумкин",
                reply_markup=await inline.download_cert(),
            )
            await state.set_state(states.UserRegistration.cert)
        else:
            await message.answer(
                text='📲 Телефон рақамингизни <b>+9989** *** ** **</b> шаклда \nюборинг, ёки <b>"📱 Рақам юбориш"</b> тугмасини босинг:', reply_markup=reply.phone_keyboard()
            )
            await state.set_state(states.UserRegistration.phone)

    class Phone:
        @user_router.message(states.UserRegistration.phone, F.contact.phone_number)
        async def user_contact(message: Message, state: FSMContext):
            await state.update_data(phone=message.contact.phone_number)
            await message.reply(
                text="✍🏼 <b>Фамилия, Исм, Шариф</b>ни киритинг.\n<i>Мисол учун: Умаров Азизбeк Иброҳим(ович) ўғли</i>"
            )
            await state.set_state(states.UserRegistration.fullname)


        @user_router.message(
            states.UserRegistration.phone,
            F.text.replace(" ", "").replace('+', '').regexp(r"^998\d{9}$"),
        )
        async def user_phone_number(message: Message, state: FSMContext):
            await state.update_data(phone=message.text.replace("+", ""))
            await message.reply(
                text="✍🏼 <b>Фамилия, Исм, Шариф</b>ни киритинг.\n<i>Мисол учун: Умаров Азизбeк Иброҳим(ович) ўғли</i>"
            )
            await state.set_state(states.UserRegistration.fullname)


        @user_router.message(states.UserRegistration.phone)
        async def user_number_incorrect(message: Message):
            await message.answer(text="❌  Телефон рақамингиз нотўғри форматда киритилган.\n☝️ Тeлeфон рақамингизни <b>+9989** *** ** **</b> шаклда\n юборинг, ёки <b>\"📱 Рақам юбориш\"</b> тугмасини босинг:")

    @user_router.message(states.UserRegistration.fullname)
    async def user_fullname(message: Message, state: FSMContext):
        if 5 < len(message.text.split()) or len(message.text.split()) < 2:
            await message.answer(
                text="✍🏼 <b>Фамилия, Исм, Шариф</b>ни киритинг.\n<i>Мисол учун: Умаров Азизбeк Иброҳим(ович) ўғли</i>"
            )
        else:
            await state.update_data(fullname=message.text)
            await message.answer(
                text="📅 Туғилган санангизни <b>кун.ой.йил</b> форматида киритинг\n<i>Мисол учун: 01.01.2000</i>"
            )
            await state.set_state(states.UserRegistration.birthday)

    @user_router.message(
        states.UserRegistration.birthday, F.text.regexp(r"^\d{2}\.\d{2}\.\d{4}$")
    )
    async def user_birthday(message: Message, state: FSMContext):
        await state.update_data(birthday=message.text)
        await message.answer(
            text="👥 Жинсингиз:", reply_markup=inline.male_female_keyboard()
        )
        await state.set_state(states.UserRegistration.malefemale)
    
    @user_router.message(states.UserRegistration.birthday)
    async def user_birthday_incorrect(message: Message):
        await message.answer(text="❌  Туғилган санангизни <b>кун.ой.йил</b> форматида киритинг\n<i>Мисол учун: 01.01.2000</i>")


class StepTwo:
    @user_router.callback_query(
        inline.Factories.MaleFemale.filter(), states.UserRegistration.malefemale
    )
    async def user_malefemale(
        call: CallbackQuery,
        callback_data: inline.Factories.MaleFemale,
        state: FSMContext,
    ):
        await state.update_data(malefemale=callback_data.id)
        await call.message.edit_text(text="🚜 Фермер ёки деҳқон хўжалиги номини киритинг")
        await state.set_state(states.UserRegistration.fermer_xojalik)

    @user_router.message(states.UserRegistration.fermer_xojalik)
    async def user_fermer_xojalik(message: Message, state: FSMContext):
        await state.update_data(fermer_xojalik=message.text)
        await message.answer(
            text="🧑‍🌾 Сизнинг лавозимингиз", reply_markup=await inline.position_keyboard()
        )
        await state.set_state(states.UserRegistration.position)

    @user_router.callback_query(
        inline.Factories.Position.filter(), states.UserRegistration.position
    )
    async def address(
        call: CallbackQuery, callback_data: inline.Factories.Position, state: FSMContext
    ):
        await state.update_data(lavozim=callback_data.id)
        await call.message.edit_text(
            text="📍 Фермер ёки деҳқон хўжалиги жойлашган ҳудудингизни танланг",
            reply_markup=await inline.regions_keyboard(),
        )
        await state.set_state(states.UserRegistration.address_region)

    @user_router.callback_query(
        inline.Factories.Region.filter(), states.UserRegistration.address_region
    )
    async def address_region(
        call: CallbackQuery, callback_data: inline.Factories.Region, state: FSMContext
    ):
        await state.update_data(region=callback_data.id)
        await call.message.edit_text(
            text="📍 Фермер ёки деҳқон хўжалиги жойлашган ҳудудингизни танланг",
            reply_markup=await inline.district_keyboard(),
        )
        await state.set_state(states.UserRegistration.address_district)

    @user_router.callback_query(
        inline.Factories.District.filter(), states.UserRegistration.address_district
    )
    async def address_region(
        call: CallbackQuery, callback_data: inline.Factories.District, state: FSMContext
    ):
        await state.update_data(district=callback_data.id)
        await call.message.edit_text(
            text="⚙️ Фермер ва деҳқон хўжалиги фаолият тури",
            reply_markup=await inline.faoliyat_turi_keyboard(),
        )
        await state.set_state(states.UserRegistration.faoliyat_turi)


class StepThree:
    @user_router.callback_query(
        inline.Factories.FaoliyatTuri.filter(), states.UserRegistration.faoliyat_turi
    )
    async def address_region(
        call: CallbackQuery, callback_data: inline.Factories.District, state: FSMContext
    ):
        await state.update_data(faoliyat_turi=callback_data.id, id_number="202300001")
        await call.message.edit_text(
            text="✅Сиз муваффақиятли рўйхатдан ўтдингиз.\n🆔Сизнинг <b>ID рақамингиз</b> 202300001.\n\n🎫Курс якунлангандан сўнг, шу ерда <b>сертификатингизни</b> юклаб олишингиз мумкин",
            reply_markup=await inline.download_cert(),
        )
        await state.set_state(states.UserRegistration.cert)

    @user_router.callback_query(
        inline.Factories.Certificate.filter(), states.UserRegistration.cert
    )
    async def cert_answer(
        call: CallbackQuery,
        callback_data: inline.Factories.Certificate,
        state: FSMContext,
    ):
        await call.answer(
            text="Курс хали якунланмаган\nКурс якунлангандан сўнг сертификатингизни юклаб олишингиз мумкин ",
            show_alert=True,
        )
