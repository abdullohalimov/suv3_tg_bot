from datetime import date
import logging
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
import tgbot.misc.states as states
import tgbot.services.api as api
import tgbot.keyboards.inline as inline
import tgbot.keyboards.reply as reply
from tgbot.misc.states import i18nn as _
from aiogram.types import BufferedInputFile

user_router = Router()


@user_router.message(F.text == "🔙 Орқага")
@user_router.message(F.text == "🔙 Назад")
@user_router.message(F.text == "🔙 Orqaga")
async def back(message: Message, state: FSMContext):
    state2 = await state.get_state()
    data = await state.get_data()
    if state2 == states.UserRegistration.phone:
        await StepOne.start(message, state)
    elif state2 == states.UserRegistration.firstname:
        await message.answer(
            text=_(
                '📲 Телефон рақамингизни <b>+9989** *** ** **</b> шаклда \nюборинг, ёки <b>"📱 Рақам юбориш"</b> тугмасини босинг:',
                locale=data.get("language"),
            ),
            reply_markup=reply.phone_keyboard(data.get("language")),
        )
        await state.set_state(states.UserRegistration.phone)
    elif state2 == states.UserRegistration.lastname:
        await message.reply(
            text=_(
                "✍🏼 <b>Исмингиз</b>ни киритинг.\n<i>Мисол учун: Азизбeк</i>",
                locale=data.get("language"),
            ),
            reply_markup=reply.back_keyboard(data.get("language")),
        )
        await state.set_state(states.UserRegistration.firstname)
    elif state2 == states.UserRegistration.secondname:
        await message.answer(
            text=_(
                "✍🏼 <b>Фамилиянгиз</b>ни киритинг.\n<i>Мисол учун: Умаров</i>",
                locale=data.get("language"),
            ),
            reply_markup=reply.back_keyboard(data.get("language")),
        )
        await state.set_state(states.UserRegistration.lastname)
    elif state2 == states.UserRegistration.birthday:
        await message.answer(
            text=_(
                "✍🏼 <b>Шарифингиз</b>ни киритинг.\n<i>Мисол учун: Иброҳимович ёки Иброҳим ўғли</i>",
                locale=data.get("language"),
            ),
            reply_markup=reply.back_keyboard(data.get("language")),
        )
        await state.set_state(states.UserRegistration.secondname)
    elif state2 == states.UserRegistration.fermer_xojalik:
        await message.answer(
            text=_("👥 Жинсингиз:", locale=data.get("language")),
            reply_markup=inline.male_female_keyboard(data.get("language")),
        )
        await state.set_state(states.UserRegistration.malefemale)
    elif state2 == states.UserRegistration.cert2:
        await state.clear()
        await message.answer(
            "Тилни танланг..\nВыберите язык..\nTilni tanlang..",
            reply_markup=inline.language_keyboard(),
        )


@user_router.callback_query(inline.Factories.Back.filter())
async def user_back(
    callback: CallbackQuery, callback_data: inline.Factories.Back, state: FSMContext
):
    state2 = await state.get_state()
    data = await state.get_data()
    if state2 == states.UserRegistration.malefemale:
        await callback.message.answer(
            text=_(
                "📅 Туғилган санангизни <b>кун.ой.йил</b> форматида киритинг\n<i>Мисол учун: 21.01.2001</i>",
                locale=data.get("language"),
            ),
            reply_markup=reply.back_keyboard(data.get("language")),
        )
        await state.set_state(states.UserRegistration.birthday)
    elif state2 == states.UserRegistration.position:
        await callback.message.edit_text(
            text=_(
                "🚜 Фермер ёки деҳқон хўжалиги номини киритинг",
                locale=data.get("language"),
            )
        )
        await state.set_state(states.UserRegistration.fermer_xojalik)
    elif state2 == states.UserRegistration.address_region:
        await callback.message.edit_text(
            text=_("🧑‍🌾 Сизнинг лавозимингиз", locale=data.get("language")),
            reply_markup=await inline.position_keyboard(data.get("language")),
        )
        await state.set_state(states.UserRegistration.position)
    elif state2 == states.UserRegistration.address_district:
        await callback.message.edit_text(
            text=_(
                "📍 Фермер ёки деҳқон хўжалиги жойлашган ҳудудингизни танланг",
                locale=data.get("language"),
            ),
            reply_markup=await inline.region_inline_keyboard(data.get("language")),
        )
        await state.set_state(states.UserRegistration.address_region)

    elif state2 == states.UserRegistration.faoliyat_turi:
        await callback.message.edit_text(
            text=_(
                "📍 Фермер ёки деҳқон хўжалиги жойлашган ҳудудингизни танланг",
                locale=data.get("language"),
            ),
            reply_markup=await inline.district_inline_keyboard(
                data.get("region"), data.get("language")
            ),
        )
        await state.set_state(states.UserRegistration.address_district)


class StepOne:
    @user_router.message(CommandStart())
    async def start(message: Message, state: FSMContext):
        await message.answer(
            "Тилни танланг..\nВыберите язык..\nTilni tanlang..",
            reply_markup=inline.language_keyboard(),
        )
        await state.set_state(states.UserRegistration.language)

    @user_router.callback_query(inline.Factories.Language.filter())
    async def user_phone(
        callback: CallbackQuery,
        callback_data: inline.Factories.Language,
        state: FSMContext,
    ):
        await state.update_data(language=callback_data.language)
        data = await state.get_data()
        if data.get("id_number"):
            await callback.message.answer(
                text=_(
                    "✅Сиз муваффақиятли рўйхатдан ўтгансиз.\n🆔Сизнинг <b>ID рақамингиз</b> {certificate_id}.\n\n🎫Курс якунлангандан сўнг, шу ерда <b>сертификатингизни</b> юклаб олишингиз мумкин",
                    locale=data.get("language"),
                ).format(certificate_id=data.get("id_number")),
                reply_markup=await inline.download_cert(data.get("language")),
            )
            await state.set_state(states.UserRegistration.cert)
        else:
            await callback.message.answer(
                text=_(
                    '📲 Телефон рақамингизни <b>+9989** *** ** **</b> шаклда \nюборинг, ёки <b>"📱 Рақам юбориш"</b> тугмасини босинг:',
                    locale=data.get("language"),
                ),
                reply_markup=reply.phone_keyboard(data.get("language")),
            )
            await state.set_state(states.UserRegistration.phone)

    class Phone:
        @user_router.message(
            states.UserRegistration.phone,
            F.contact.phone_number
            | F.text.replace(" ", "").replace("+", "").regexp(r"^998\d{9}$"),
        )
        async def user_contact(message: Message, state: FSMContext):
            try:
                await state.update_data(
                    phone=message.contact.phone_number.replace(" ", "").replace("+", "")
                )
            except:
                await state.update_data(
                    phone=message.text.replace(" ", "").replace("+", "")
                )
            data = await state.get_data()
            check = await api.check_phone(data.get("phone"))
            if check["success"]:
                await message.reply(
                    text=_(
                        "✍🏼 <b>Исмингиз</b>ни киритинг.\n<i>Мисол учун: Азизбeк</i>",
                        locale=data.get("language"),
                    ),
                    reply_markup=reply.back_keyboard(data.get("language")),
                )
                await state.set_state(states.UserRegistration.firstname)
            else:
                await message.answer(
                    _(
                        "Ушбу фойдаланувчи аввал ройхатдан утган. Сертификатни юклаб олиш учун ID ракамингизни киритинг",
                        locale=data.get("language"),
                    )
                )
                await state.set_state(states.UserRegistration.cert2)
                await message.delete()

        @user_router.message(states.UserRegistration.phone)
        async def user_number_incorrect(message: Message, state: FSMContext):
            data = await state.get_data()
            await message.answer(
                text=_(
                    '❌  Телефон рақамингиз нотўғри форматда киритилган.\n☝️ Тeлeфон рақамингизни <b>+9989** *** ** **</b> шаклда\n юборинг, ёки <b>"📱 Рақам юбориш"</b> тугмасини босинг:',
                    locale=data.get("language"),
                ),
                reply_markup=reply.phone_keyboard(data.get("language")),
            )

    class Fio:
        @user_router.message(states.UserRegistration.firstname)
        async def user_firstname(message: Message, state: FSMContext):
            data = await state.get_data()
            await state.update_data(f_name=message.text)
            await message.answer(
                text=_(
                    "✍🏼 <b>Фамилиянгиз</b>ни киритинг.\n<i>Мисол учун: Умаров</i>",
                    locale=data.get("language"),
                ),
                reply_markup=reply.back_keyboard(data.get("language")),
            )
            await state.set_state(states.UserRegistration.lastname)

        @user_router.message(states.UserRegistration.lastname)
        async def user_lastname(message: Message, state: FSMContext):
            data = await state.get_data()

            await state.update_data(l_name=message.text)
            await message.answer(
                text=_(
                    "✍🏼 <b>Шарифингиз</b>ни киритинг.\n<i>Мисол учун: Иброҳимович ёки Иброҳим ўғли</i>",
                    locale=data.get("language"),
                ),
                reply_markup=reply.back_keyboard(data.get("language")),
            )
            await state.set_state(states.UserRegistration.secondname)

        @user_router.message(states.UserRegistration.secondname)
        async def user_fullname(message: Message, state: FSMContext):
            await state.update_data(s_name=message.text)
            data = await state.get_data()

            await message.answer(
                text=_(
                    "📅 Туғилган санангизни <b>кун.ой.йил</b> форматида киритинг\n<i>Мисол учун: 21.01.2001</i>",
                    locale=data.get("language"),
                ),
                reply_markup=reply.back_keyboard(data.get("language")),
            )
            await state.set_state(states.UserRegistration.birthday)

    class Birthday:
        @user_router.message(
            states.UserRegistration.birthday, F.text.regexp(r"^\d{2}\.\d{2}\.\d{4}$")
        )
        async def user_birthday(message: Message, state: FSMContext):
            birthdayy = message.text.split(".")
            if (
                1945 <= int(birthdayy[2]) <= date.today().year
                and int(birthdayy[1]) <= 12
                and int(birthdayy[0]) <= 31
            ):
                birthd = f"{birthdayy[2]}-{birthdayy[1]}-{birthdayy[0]}"
                await state.update_data(birthday=birthd)
                data = await state.get_data()

                await message.answer(
                    text=_("👥 Жинсингиз:", locale=data.get("language")),
                    reply_markup=inline.male_female_keyboard(data.get("language")),
                )
                await state.set_state(states.UserRegistration.malefemale)
            else:
                await StepOne.Birthday.user_birthday_incorrect(message, state)

        @user_router.message(states.UserRegistration.birthday)
        async def user_birthday_incorrect(message: Message, state: FSMContext):
            data = await state.get_data()

            await message.answer(
                text=_(
                    "❌  Туғилган санангизни <b>кун.ой.йил</b> форматида киритинг\n<i>Мисол учун: 21.01.2001</i>",
                    locale=data.get("language"),
                ),
                reply_markup=reply.back_keyboard(data.get("language")),
            )

    class Gender:
        @user_router.callback_query(
            inline.Factories.MaleFemale.filter(), states.UserRegistration.malefemale
        )
        async def user_malefemale(
            call: CallbackQuery,
            callback_data: inline.Factories.MaleFemale,
            state: FSMContext,
        ):
            await state.update_data(gender=callback_data.id)
            data = await state.get_data()
            request1 = await api.step_one_request(data)
            if request1["success"]:
                await call.message.edit_text(
                    text=_(
                        "🚜 Фермер ёки деҳқон хўжалиги номини киритинг",
                        locale=data.get("language"),
                    )
                )
                await state.set_state(states.UserRegistration.fermer_xojalik)
            else:
                await call.message.answer(
                    _(
                        "Ушбу фойдаланувчи аввал ройхатдан утган. Сертификатни юклаб олиш учун ID ракамингизни киритинг",
                        locale=data.get("language"),
                    )
                )
                await state.set_state(states.UserRegistration.cert2)
                await call.message.delete()


class StepTwo:
    @user_router.message(states.UserRegistration.fermer_xojalik)
    async def user_fermer_xojalik(message: Message, state: FSMContext):
        await state.update_data(farm_name=message.text)
        data = await state.get_data()

        await message.answer(
            text=_("🧑‍🌾 Сизнинг лавозимингиз", locale=data.get("language")),
            reply_markup=await inline.position_keyboard(data.get("language")),
        )
        await state.set_state(states.UserRegistration.position)

    @user_router.callback_query(
        inline.Factories.Position.filter(), states.UserRegistration.position
    )
    async def address(
        call: CallbackQuery, callback_data: inline.Factories.Position, state: FSMContext
    ):
        await state.update_data(position=callback_data.id)
        data = await state.get_data()

        await call.message.edit_text(
            text=_(
                "📍 Фермер ёки деҳқон хўжалиги жойлашган ҳудудингизни танланг",
                locale=data.get("language"),
            ),
            reply_markup=await inline.region_inline_keyboard(data.get("language")),
        )
        await state.set_state(states.UserRegistration.address_region)

    @user_router.callback_query(
        inline.Factories.Region.filter(), states.UserRegistration.address_region
    )
    async def address_region(
        call: CallbackQuery, callback_data: inline.Factories.Region, state: FSMContext
    ):
        await state.update_data(region=callback_data.id)
        data = await state.get_data()

        await call.message.edit_text(
            text=_(
                "📍 Фермер ёки деҳқон хўжалиги жойлашган ҳудудингизни танланг",
                locale=data.get("language"),
            ),
            reply_markup=await inline.district_inline_keyboard(
                callback_data.id, data.get("language")
            ),
        )
        await state.set_state(states.UserRegistration.address_district)

    @user_router.callback_query(
        inline.Factories.District.filter(), states.UserRegistration.address_district
    )
    async def address_district(
        call: CallbackQuery, callback_data: inline.Factories.District, state: FSMContext
    ):
        await state.update_data(district_id=callback_data.id)
        data = await state.get_data()

        await call.message.edit_text(
            text=_(
                "⚙️ Фермер ва деҳқон хўжалиги фаолият тури", locale=data.get("language")
            ),
            reply_markup=await inline.faoliyat_turi_keyboard(data.get("language")),
        )
        await state.set_state(states.UserRegistration.faoliyat_turi)


class StepThree:
    @user_router.callback_query(
        inline.Factories.FaoliyatTuri.filter(), states.UserRegistration.faoliyat_turi
    )
    async def address_region(
        call: CallbackQuery, callback_data: inline.Factories.District, state: FSMContext
    ):
        await state.update_data(farm_type=callback_data.id)
        data = await state.get_data()

        request2 = await api.step_two_request(data)
        if request2["success"]:
            await state.update_data(certificate_id=request2["data"]["certificate_id"])
            await call.message.edit_text(
                text=_(
                    "✅Сиз муваффақиятли рўйхатдан ўтдингиз.\n🆔Сизнинг <b>ID рақамингиз</b> {id_number}.\n\n🎫Курс якунлангандан сўнг, шу ерда <b>сертификатингизни</b> юклаб олишингиз мумкин",
                    locale=data.get("language"),
                ).format(id_number=request2["data"]["certificate_id"]),
                reply_markup=await inline.download_cert(data.get("language")),
            )
            await state.set_state(states.UserRegistration.cert)

        else:
            await call.message.answer(
                _(
                    "Ушбу фойдаланувчи аввал ройхатдан утган. Сертификатни юклаб олиш учун ID ракамингизни киритинг",
                    locale=data.get("language"),
                ),
                reply_markup=reply.back_keyboard(data.get("language")),
            )
            await state.set_state(states.UserRegistration.cert2)

    @user_router.callback_query(
        inline.Factories.Certificate.filter(), states.UserRegistration.cert
    )
    async def cert_answer(
        call: CallbackQuery,
        callback_data: inline.Factories.Certificate,
        state: FSMContext,
    ):
        data = await state.get_data()
        request = await api.certificate_download(data["certificate_id"])
        if request:
            await call.message.answer_document(
                document=BufferedInputFile(
                    request,
                    filename="certificate-{cert_id}.pdf".format(
                        cert_id=data["certificate_id"]
                    ),
                )
            )
            await call.answer()
        else:
            await call.answer(
                text=_(
                    "⏳ Курс хали якунланмаган\nКурс якунлангандан сўнг сертификатингизни юклаб олишингиз мумкин",
                    locale=data.get("language"),
                ),
                show_alert=True,
            )

    @user_router.message(states.UserRegistration.cert2, F.text.isdigit())
    async def cert_number(message: Message, state: FSMContext):
        data = await state.get_data()

        request = await api.certificate_download(message.text)
        if request:
            await message.answer_document(
                document=BufferedInputFile(
                    request,
                    filename="certificate-{cert_id}.pdf".format(cert_id=message.text),
                )
            )
        else:
            await message.answer(
                _(
                    "❔ID нотогри киритилди ёки курс хали якунланмаган\n⏳ Курс якунлангандан сўнг сертификатингизни юклаб олишингиз мумкин",
                    locale=data.get("language"),
                )
            )
