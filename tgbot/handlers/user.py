from datetime import date, datetime
import logging
from aiogram import F, Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
import tgbot.misc.states as states
import tgbot.services.api as api
import tgbot.keyboards.inline as inline
import tgbot.keyboards.reply as reply
from tgbot.misc.states import i18nn as _
from aiogram.types import BufferedInputFile, FSInputFile
import re
from tgbot.services.db import Score
from tgbot.misc.regions_with_teachers import returnn_teachers
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Protection
from tgbot.filters.admin import AdminFilter


user_router = Router()
today = datetime.now().day
admins_list = [
    "541457443",
    "562738727",
    "1357813137",
    ]
moders_list = [
    "143659989",
    "1441325781",
    "1017075026",
    "604092057",
    "5557914805",
    "1703817316",
]
limited_admins = {
    "143659989": 0,
    "1441325781": 0,
    "1017075026": 0,
    "604092057": 0,
    "5557914805": 0,
    "1703817316": 0,
}
actual_limited_admins = {
    "143659989": 0,
    "1441325781": 0,
    "1017075026": 0,
    "604092057": 0,
    "5557914805": 0,
    "1703817316": 0,
}

def making_excel(data: list):
    wb = Workbook()
    ws = wb.active
    ws.title = "So'rovnoma"
    values = [
        "ID",
        "FIO",
        "Viloyat",
        "Tuman",
        "Universitet professori",
        "Turk mutaxassisi",
        "Bank mutaxassisi",
        "Vazirlik mutaxassisi",
        "Tashkiliy jarayonlar",
        "Fikrlar",
    ]
    alignment = Alignment(wrap_text=True, shrink_to_fit=False, indent=0)
    protection = Protection(locked=False, hidden=False)
    print(values)
    ws.append(values)
    ft = Font(bold=True)
    for row in ws["A1:I1"]:
        for cell in row:
            cell.font = ft
            cell.alignment = alignment
            cell.protection = protection
    already_added: set = set()
    to_add = []
    for i in reversed(data):
        if i[0] in already_added:
            pass
        else:
            already_added.add(i[0])
            to_add.append(i)
    for i in reversed(to_add):
        ws.append(i)

    ws.column_dimensions["A"].width = 8
    ws.column_dimensions["B"].width = 30
    ws.column_dimensions["C"].width = 30
    ws.column_dimensions["D"].width = 30
    ws.column_dimensions["E"].width = 12
    ws.column_dimensions["F"].width = 12
    ws.column_dimensions["G"].width = 12
    ws.column_dimensions["H"].width = 12
    ws.column_dimensions["I"].width = 12
    ws.column_dimensions["J"].width = 30

    wb.save("sorovnoma.xlsx")


async def is_subscribed(user_id, channels_id, bot: Bot) -> bool:
    chat_member = await bot.get_chat_member(chat_id=channels_id, user_id=user_id)

    return chat_member.status


@user_router.message(F.text == "🔙 Орқага")
# @user_router.message(F.text == "🔙 Назад")
@user_router.message(F.text == "🔙 Orqaga")
async def back(message: Message, state: FSMContext, bot: Bot):
    # await channel_check(bot, message)
    state2 = await state.get_state()
    data = await state.get_data()
    if state2 == states.UserRegistration.phone:
        await StepOne.start(message, state)
    elif state2 == states.UserRegistration.full_name:
        await message.answer(
            text=_(
                '<b>"📱 Рақам юбориш"</b> тугмасини босинг ва телефон рақамингизни юборинг',  # '📲 Телефон рақамингизни <b>+9989** *** ** **</b> шаклда \nюборинг, ёки <b>"📱 Рақам юбориш"</b> тугмасини босинг:',
                locale=data.get("language"),
            ),
            reply_markup=reply.phone_keyboard(data.get("language")),
        )
        await state.set_state(states.UserRegistration.phone)
    elif state2 == states.UserRegistration.birthday:
        await message.answer(
            text=_(
                "✍🏼 <b>Фамилия, Исм, Шарифингиз</b>ни киритинг.\n<i>Мисол учун: Азимов Азизбeк Азизович</i>",
                locale=data.get("language"),
            ),
            reply_markup=reply.back_keyboard(data.get("language")),
        )
        await state.set_state(states.UserRegistration.full_name)
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
                "🚜 Фермер/деҳқон хўжалиги ёки ташкилотингиз номи",
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
            "Тилни танланг..\n\nTilni tanlang..",
            reply_markup=inline.language_keyboard(),
        )
        await state.set_state(states.UserRegistration.language)

    @user_router.callback_query(inline.Factories.Language.filter())
    async def user_phone(
        callback: CallbackQuery,
        callback_data: inline.Factories.Language,
        state: FSMContext,
        bot: Bot,
    ):
        if callback_data.language == "check":
            pass
        else:
            await state.update_data(language=callback_data.language)
        if True:
            data = await state.get_data()
            subscribe = await is_subscribed(
                user_id=callback.message.chat.id, channels_id="-1001876037953", bot=bot
            )
            #  don't forget to change back
            # subscribe = "right"
            if subscribe == "left":
                # await message.answer(text='Not subscribed')
                await callback.answer(
                    text=_(
                        "Ҳурматли иштирокчи! Сўровномани давом эттириш учун Сувчилар мактаби расмий телеграм каналига аъзо бўлишингизни сўраймиз!",
                        locale=data.get("language"),
                    ),
                    show_alert=True,
                )
                if callback_data.language == "check":
                    pass
                else:
                    await callback.message.answer(
                        _(
                            "Ҳурматли иштирокчи! Сўровномани давом эттириш учун Сувчилар мактаби расмий телеграм каналига аъзо бўлишингизни сўраймиз!",
                            locale=data.get("language"),
                        ),
                        reply_markup=await inline.channels_keyboard(
                            data.get("language")
                        ),
                    )
                    await callback.message.delete()

            else:
                await callback.message.answer(
                    text=_(
                        '<b>"📱 Рақам юбориш"</b> тугмасини босинг ва телефон рақамингизни юборинг',  # '📲 Телефон рақамингизни <b>+9989** *** ** **</b> шаклда \nюборинг, ёки <b>"📱 Рақам юбориш"</b> тугмасини босинг:',
                        locale=data.get("language"),
                    ),
                    reply_markup=reply.phone_keyboard(data.get("language")),
                )
                await state.set_state(states.UserRegistration.phone)
        else:
            await callback.answer(
                text=_(
                    '"Сувчилар мактаби"да ўқув жараёнлари учун рўйхатдан ўтиш 1-июн соат 9. 30 дан бошланишини маълум қиламиз!',
                    locale=callback_data.language,
                ),
                show_alert=True,
            )

    class Phone:
        @user_router.message(
            states.UserRegistration.phone,
            F.contact.phone_number | F.text.replace(" ", "").replace("+", ""),
        )
        async def user_contact(message: Message, state: FSMContext):
            data = await state.get_data()
            try:
                await state.update_data(
                    phone=message.contact.phone_number.replace(" ", "").replace("+", "")
                )
            except:
                global today
                global actual_limited_admins
                
                if datetime.now().day != today:
                    today = datetime.now().day
                    actual_limited_admins = limited_admins
                user_id = str(message.chat.id)
                if user_id in admins_list:
                    continuee = True
                    is_admin = True
                elif user_id in moders_list:
                    continuee = True
                    is_admin = False # but he's moder
                else:
                    continuee = False

                if continuee:
                    if actual_limited_admins.get(user_id, 16) < 15 or is_admin:
                        regexp = r"^\d{12}$"
                        number = (
                            message.text.replace(" ", "")
                            .replace("+", "")
                            .replace("secret", "")
                        )
                        if re.match(regexp, number):
                            await state.update_data(phone=number)
                            if not is_admin:
                                actual_limited_admins[user_id] += 1
                        else:
                            await message.answer(
                                text=_(
                                    '❌  Телефон рақамингиз нотўғри форматда киритилган.\n☝️ Тeлeфон рақамингизни <b>+9989** *** ** **</b> шаклда\n юборинг, ёки <b>"📱 Рақам юбориш"</b> тугмасини босинг:',
                                    locale=data.get("language"),
                                ),
                                reply_markup=reply.phone_keyboard(data.get("language")),
                            )
                            return
                    else:
                        await message.answer(_("Кунлик лимит нихоясига етган", locale=data.get("language")))
                        return
                else:
                    await message.delete()
                    return
            data = await state.get_data()
            check = await api.check_phone(data.get("phone"))
            if check["success"]:
                await message.answer(
                    text=_(
                        "✍🏼 <b>ФИШ\nФамилия, Исм, Шарифингиз</b>ни киритинг.\n<i>Мисол учун: Азимов Азизбeк Азизович</i>",
                        locale=data.get("language"),
                    ),
                    reply_markup=reply.back_keyboard(data.get("language")),
                )
                await state.set_state(states.UserRegistration.full_name)
            else:
                await message.answer(
                    _(
                        "❕ Ушбу фойдаланувчи аввал рўйхатдан ўтган. Сертификатни юклаб олиш учун ID рақамингизни киритинг",
                        locale=data.get("language"),
                    )
                )
                await state.set_state(states.UserRegistration.cert2)
                await message.delete()

        @user_router.message(states.UserRegistration.phone, AdminFilter())
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
        @user_router.message(states.UserRegistration.full_name)
        async def user_fullname(message: Message, state: FSMContext):
            data = await state.get_data()
            if 6 > len(message.text.split()) >= 2:
                await state.update_data(full_name=message.text)

                await message.answer(
                    text=_(
                        "📍 Фермер ёки деҳқон хўжалиги жойлашган ҳудудингизни танланг",
                        locale=data.get("language"),
                    ),
                    reply_markup=await inline.region_inline_keyboard(
                        data.get("language")
                    ),
                )
                await state.set_state(states.UserRegistration.address_region)

            else:
                await message.delete()
                await message.answer(
                    _(
                        "❌ <b>ФИШ\nФамилия, Исм, Шарифингиз</b> хато киритилди\n\n✅ <i>Мисол учун: Азимов Азизбeк Азизович</i>\n\n✍🏼 <b>Фамилия, Исм, Шарифингиз</b>ни қайтадан киритинг.",
                        locale=data.get("language"),
                    ),
                    reply_markup=reply.back_keyboard(data.get("language")),
                )


class Address:
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
        await call.message.answer(
            text=_(
                "📅 Туғилган санангизни <b>кун.ой.йил</b> форматида киритинг\n<i>Мисол учун: 21.01.2001</i>",
                locale=data.get("language"),
            ),
            reply_markup=reply.back_keyboard(data.get("language")),
        )
        await state.set_state(states.UserRegistration.birthday)
        await call.message.delete()

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
                await Address.Birthday.user_birthday_incorrect(message, state)

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
            request1 = await api.step_one_request(data, call.from_user.id)
            if request1["success"]:
                await call.message.edit_text(
                    text=_(
                        "🚜 Фермер/деҳқон хўжалиги ёки ташкилотингиз номи",
                        locale=data.get("language"),
                    )
                )
                await state.set_state(states.UserRegistration.fermer_xojalik)
            else:
                await call.message.answer(
                    _(
                        "❕ Ушбу фойдаланувчи аввал рўйхатдан ўтган. Сертификатни юклаб олиш учун ID рақамингизни киритинг",
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
    async def position(
        call: CallbackQuery, callback_data: inline.Factories.Position, state: FSMContext
    ):
        await state.update_data(position=callback_data.id)
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
                    "✅Сиз муваффақиятли рўйхатдан ўтдингиз.\n🆔Сизнинг <b>ID рақамингиз</b> {id_number}.\n\n🎫Курс якунланганидан сўнг, шу ерда <b>сертификатингизни</b> юклаб олишингиз мумкин",
                    locale=data.get("language"),
                ).format(id_number=request2["data"]["certificate_id"]),
                reply_markup=await inline.download_cert(data.get("language")),
            )
            await state.set_state(states.UserRegistration.cert)

        else:
            await call.message.answer(
                _(
                    "❕ Ушбу фойдаланувчи аввал рўйхатдан ўтган. Сертификатни юклаб олиш учун ID рақамингизни киритинг",
                    locale=data.get("language"),
                ),
                reply_markup=reply.back_keyboard(data.get("language")),
            )
            await state.set_state(states.UserRegistration.cert2)

    @user_router.callback_query(inline.Factories.Certificate.filter())
    async def cert_answer(
        call: CallbackQuery,
        callback_data: inline.Factories.Certificate,
        state: FSMContext,
        bot: Bot,
    ):
        data = await state.get_data()

        wait = await call.message.answer(
            text=_("⏳ Юкланмоқда, кутиб туринг...", locale=data.get("language"))
        )
        request = await api.get_user_data_from_cert_id(data.get("certificate_id"))
        if int(request.get("data", False).get("status", 0)) == 3:
            # await message.answer_document(
            #     document=BufferedInputFile(
            #         request,
            #         filename="certificate-{cert_id}.pdf".format(cert_id=message.text),
            #     )
            # )
            teachers = returnn_teachers(
                int(request["data"]["region_id"]), data.get("language")
            )

            await call.message.answer(
                _(
                    "<b>Сертификатни юклаб олиш учун қуйидаги сўровномани тўлдиринг.</b>",
                    locale=data.get("language"),
                )
            )
            # await message.answer(_('<b>Вилоятингизни танланг:</b>', locale=data.get("language")), reply_markup=await inline.region_inline_keyboard(data.get("language"), False))
            # await state.set_state(states.Survey.test)
            await state.update_data(
                certificate_id=data.get("certificate_id"), teachers=teachers
            )
            await state.set_state(states.UserStates.first)
            await call.message.answer(
                _(
                    "<b>Университет профессор-ўқитувчисини баҳоланг</b>\n<b>Ф.И.Ш:</b> <i>{teacher}</i>\n<b>Маъруза мавзуси:</b> <i>Сув тежовчи технологияларнинг афзалликлари ва уларни самарадорлиги</i>",
                    locale=data.get("language"),
                ).format(teacher=teachers["professor"]),
                reply_markup=await inline.score_keyboard(1, data.get("language")),
            )
        else:
            await call.answer(
                text=_(
                    "⏳ Курс ҳали якунланмаган\nКурс якунланганидан сўнг сертификатингизни юклаб олишингиз мумкин",
                    locale=data.get("language"),
                ),
                show_alert=True,
            )

        await wait.delete()

    @user_router.message(states.UserRegistration.cert2, F.text.isdigit())
    async def cert_number(message: Message, state: FSMContext, bot: Bot):
        data = await state.get_data()

        wait = await message.answer(
            text=_("⏳ Юкланмоқда, кутиб туринг...", locale=data.get("language"))
        )
        request = await api.get_user_data_from_cert_id(message.text)
        if int(request.get("data", {"status": False}).get("status", 0)) == 3:
            # await message.answer_document(
            #     document=BufferedInputFile(
            #         request,
            #         filename="certificate-{cert_id}.pdf".format(cert_id=message.text),
            #     )
            # )
            teachers = returnn_teachers(
                int(request["data"]["region_id"]), data.get("language")
            )

            await message.answer(
                _(
                    "<b>Сертификатни юклаб олиш учун қуйидаги сўровномани тўлдиринг.</b>",
                    locale=data.get("language"),
                )
            )
            # await message.answer(_('<b>Вилоятингизни танланг:</b>', locale=data.get("language")), reply_markup=await inline.region_inline_keyboard(data.get("language"), False))
            # await state.set_state(states.Survey.test)
            await state.update_data(certificate_id=message.text, teachers=teachers)
            await state.set_state(states.UserStates.first)
            await message.answer(
                _(
                    "<b>Университет профессор-ўқитувчисини баҳоланг</b>\n<b>Ф.И.Ш:</b> <i>{teacher}</i>\n<b>Маъруза мавзуси:</b> <i>Сув тежовчи технологияларнинг афзалликлари ва уларни самарадорлиги</i>",
                    locale=data.get("language"),
                ).format(teacher=teachers["professor"]),
                reply_markup=await inline.score_keyboard(1, data.get("language")),
            )

        else:
            await message.answer(
                _(
                    "❔ Ушбу ID топилмади ёки курс ҳали якунланмаган\n⏳ Курс якунланганидан сўнг сертификатингизни юклаб олишингиз мумкин",
                    locale=data.get("language"),
                )
            )

        # await bot.delete_message(chat_id=message.from_user.id, message_id=wait.message_id)
        await wait.delete()


class Survey:
    # @user_router.message(F.text == "/survey")
    # async def user_start(message: Message, state: FSMContext):

    # @user_router.callback_query(
    #     inline.Factories.Region.filter(), states.Survey.test
    # )
    # async def user_start(callback: CallbackQuery, callback_data: inline.Factories.Region, state: FSMContext):
    #     data = await state.get_data()
    #     message = callback.message

    @user_router.callback_query(
        states.UserStates.first, inline.Factories.Score.filter()
    )
    async def first_step(
        callback: CallbackQuery,
        callback_data: inline.Factories.Score,
        state: FSMContext,
    ):
        data = await state.get_data()
        teachers = data.get("teachers")
        await callback.message.answer(
            _(
                "<b>Турк мутахассисини баҳоланг</b>\n<b>Ф.И.Ш:</b> <i>{teacher}</i>\n<b>Маъруза мавзуси:</b> <i>Замонавий суғориш тизимининг аҳамияти ва сувдан фойдаланиш маданияти</i>",
                locale=data["language"],
            ).format(teacher=teachers["turk_mutaxassis"]),
            reply_markup=await inline.score_keyboard(2, data.get("language")),
        )
        await state.set_state(states.UserStates.second)
        await state.update_data(first=callback_data.id)
        await callback.message.edit_text(
            callback.message.text
            + _("\nБаҳо:  {emoji}", locale=data.get("language")).format(
                emoji=callback_data.emoji
            ),
            entities=callback.message.entities,
        )

    @user_router.callback_query(
        states.UserStates.second, inline.Factories.Score.filter()
    )
    async def second(
        callback: CallbackQuery,
        callback_data: inline.Factories.Score,
        state: FSMContext,
    ):
        data = await state.get_data()
        teachers = data.get("teachers")
        await callback.message.answer(
            _(
                "<b>Банк мутахассисини баҳоланг</b>\n<b>Ф.И.Ш:</b> <i>{teacher}</i>\n<b>Маъруза мавзуси:</b> <i>Иқтисодий ва ҳуқуқий саводхонлик:  субсидия,  кафилликлар,  солиқ имтиёзлари ва банк кредитлари</i>",
                locale=data["language"],
            ).format(teacher=teachers["bank_xodimi"]),
            reply_markup=await inline.score_keyboard(3, data.get("language")),
        )
        await state.set_state(states.UserStates.third)
        await state.update_data(second=callback_data.id)
        await callback.message.edit_text(
            callback.message.text
            + _("\nБаҳо:  {emoji}", locale=data.get("language")).format(
                emoji=callback_data.emoji
            ),
            entities=callback.message.entities,
        )

    @user_router.callback_query(
        states.UserStates.third, inline.Factories.Score.filter()
    )
    async def third(
        callback: CallbackQuery,
        callback_data: inline.Factories.Score,
        state: FSMContext,
    ):
        data = await state.get_data()
        teachers = data.get("teachers")
        await callback.message.answer(
            _(
                "<b>Сув хўжалиги вазирлиги мутахассисини баҳоланг</b>\n<b>Ф.И.Ш:</b> <i>{teacher}</i>\n<b>Маъруза мавзуси:</b> <i>Иқтисодий ва ҳуқуқий саводхонлик:  субсидия,  кафилликлар,  солиқ имтиёзлари ва банк кредитлари</i>",
                locale=data["language"],
            ).format(teacher=teachers["suv_masuli"]),
            reply_markup=await inline.score_keyboard(4, data.get("language")),
        )
        await state.set_state(states.UserStates.four)
        await state.update_data(third=callback_data.id)
        await callback.message.edit_text(
            callback.message.text
            + _("\nБаҳо:  {emoji}", locale=data.get("language")).format(
                emoji=callback_data.emoji
            ),
            entities=callback.message.entities,
        )

    @user_router.callback_query(states.UserStates.four, inline.Factories.Score.filter())
    async def four(
        callback: CallbackQuery,
        callback_data: inline.Factories.Score,
        state: FSMContext,
    ):
        data = await state.get_data()
        await callback.message.answer(
            _(
                "<b>Ўқув курси ташкилий жараёнлари</b>(ўқув материаллари, эсдалик совғалар,  тушлик ва бошқалар)<b>ни баҳоланг</b>",
                locale=data["language"],
            ),
            reply_markup=await inline.score_keyboard(5, data.get("language")),
        )
        await state.set_state(states.UserStates.five)
        await state.update_data(four=callback_data.id)
        await callback.message.edit_text(
            callback.message.text
            + _("\nБаҳо:  {emoji}", locale=data.get("language")).format(
                emoji=callback_data.emoji
            ),
            entities=callback.message.entities,
        )

    @user_router.callback_query(states.UserStates.five, inline.Factories.Score.filter())
    async def five(
        callback: CallbackQuery,
        callback_data: inline.Factories.Score,
        state: FSMContext,
    ):
        data = await state.get_data()
        await callback.message.answer(
            _(
                "<b>Ўқув курси ҳақида фикрларингиз бўлса, шу йерда ёзиб қолдиринг</b> (мажбурий эмас)",
                locale=data["language"],
            ),
            reply_markup=await inline.continue_step(data["language"]),
        )
        await state.set_state(states.UserStates.six)
        await state.update_data(five=callback_data.id)
        await callback.message.edit_text(
            callback.message.text
            + _("\nБаҳо:  {emoji}", locale=data.get("language")).format(
                emoji=callback_data.emoji
            ),
            entities=callback.message.entities,
        )

    @user_router.message(states.UserStates.six)
    async def six(message: Message, state: FSMContext):
        await state.update_data(six=message.text)
        data = await state.get_data()
        await message.answer(
            _(
                "<b>✅ Сўровномада қатнашганингиз учун миннатдормиз! </b>",
                locale=data["language"],
            )
        )
        # await state.set_state(states.UserStates.seven)
        wait = await message.answer(
            text=_("⏳ Юкланмоқда, кутиб туринг...", locale=data.get("language"))
        )
        await api.send_feedback(data=data)
        request = await api.certificate_download(data=data["certificate_id"])
        if request:
            await message.answer_document(
                document=BufferedInputFile(
                    request,
                    filename="certificate-{cert_id}.pdf".format(
                        cert_id=data["certificate_id"]
                    ),
                )
            )
            # try:
            #     record: Score = Score.get(cert_id=data["certificate_id"])
            #     record.first = data["first"]
            #     record.second = data["second"]
            #     record.third = data["third"]
            #     record.four = data["four"]
            #     record.five = data["five"]
            #     record.six = data["six"]
            #     record.cert_id = data["certificate_id"]
            #     record.save()
            # except:
            #     Score.create(
            #         first=data["first"],
            #         second=data["second"],
            #         third=data["third"],
            #         four=data["four"],
            #         five=data["five"],
            #         six=data["six"],
            #         cert_id=data["certificate_id"],
            #     )
        await wait.delete()
        await state.set_state(states.UserStates.seven)

    @user_router.callback_query(states.UserStates.six)
    async def sixdotone(callback: CallbackQuery, state: FSMContext):
        await state.update_data(six="None")
        data = await state.get_data()
        await callback.message.answer(
            _(
                "<b>✅ Сўровномада қатнашганингиз учун миннатдормиз! </b>",
                locale=data["language"],
            )
        )
        wait = await callback.message.answer(
            text=_("⏳ Юкланмоқда, кутиб туринг...", locale=data.get("language"))
        )
        # await state.set_state(states.UserStates.seven)
        await api.send_feedback(data=data)
        # return
        request = await api.certificate_download(data=data["certificate_id"])
        if request:
            await callback.message.answer_document(
                document=BufferedInputFile(
                    request,
                    filename="certificate-{cert_id}.pdf".format(
                        cert_id=data["certificate_id"]
                    ),
                )
            )
            # try:
            #     record: Score = Score.get(cert_id=data["certificate_id"])
            #     record.first = data["first"]
            #     record.second = data["second"]
            #     record.third = data["third"]
            #     record.four = data["four"]
            #     record.five = data["five"]
            #     record.six = data["six"]
            #     record.cert_id = data["certificate_id"]
            #     record.save()
            # except:
            #     Score.create(
            #         first=data["first"],
            #         second=data["second"],
            #         third=data["third"],
            #         four=data["four"],
            #         five=data["five"],
            #         six=data["six"],
            #         cert_id=data["certificate_id"],
            #     )
        await wait.delete()
        await state.set_state(states.UserStates.seven)

    @user_router.message(Command("survey"))
    async def survey_results(message: Message, state: FSMContext):
        feedbacks = await api.get_all_feedbacks()
        results = []

        for i in feedbacks["data"]:
            try:
                results.append(
                    [
                        i["request"]["id"],
                        i["request"]["full_name"],
                        i["request"]["region_name"],
                        i["request"]["district_name"],
                        i["rates"][0]["rate"],
                        i["rates"][1]["rate"],
                        i["rates"][2]["rate"],
                        i["rates"][3]["rate"],
                        i["rates"][4]["rate"],
                        i["comment"]
                        if i["comment"] != "None"
                        else "Fikr bildirilmagan",
                    ]
                )
            except:
                pass
        making_excel(results)

        await message.answer_document(FSInputFile("sorovnoma.xlsx"))
