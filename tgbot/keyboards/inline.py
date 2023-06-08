import logging
from tgbot.services import api
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from tgbot.misc.states import i18nn as _


def language_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text="Ўзбекча", callback_data=Factories.Language(language="uz").pack()
        ),
        # InlineKeyboardButton(
        #     text="🇷🇺 Русcкий", callback_data=Factories.Language(language="ru").pack()
        # ),
        InlineKeyboardButton(
            text="O'zbekcha", callback_data=Factories.Language(language="de").pack()
        ),
    )

    keyboard.adjust(1)
    return keyboard.as_markup()


def male_female_keyboard(lang):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text=_("Эркак", locale=lang),
            callback_data=Factories.MaleFemale(id="1").pack(),
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text=_("Аёл", locale=lang),
            callback_data=Factories.MaleFemale(id="2").pack(),
        )
    )
    keyboard.adjust(1)
    keyboard.row(
        InlineKeyboardButton(
            text=_("🔙 Орқага", locale=lang),
            callback_data=Factories.Back(id="back").pack(),
        )
    )
    return keyboard.as_markup()


async def position_keyboard(lang):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text=_("Хўжалик раҳбари", locale=lang),
            callback_data=Factories.Position(id=1).pack(),
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text=_("Ишчи", locale=lang), callback_data=Factories.Position(id=2).pack()
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text=_("Сувчи", locale=lang),
            callback_data=Factories.Position(id=3).pack(),
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text=_("Ирригатор", locale=lang),
            callback_data=Factories.Position(id=4).pack(),
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text=_("Банк ходими", locale=lang),
            callback_data=Factories.Position(id=5).pack(),
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text=_("Бошқа", locale=lang),
            callback_data=Factories.Position(id=6).pack(),
        )
    )

    keyboard.adjust(1)

    keyboard.row(
        InlineKeyboardButton(
            text=_("🔙 Орқага", locale=lang),
            callback_data=Factories.Back(id="back").pack(),
        )
    )

    return keyboard.as_markup()


async def faoliyat_turi_keyboard(lang):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text=_("Пахтачилик/ғаллачилик", locale=lang),
            callback_data=Factories.FaoliyatTuri(id=1).pack(),
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text=_("Боғдорчилик/узумчилик", locale=lang),
            callback_data=Factories.FaoliyatTuri(id=2).pack(),
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text=_("Сабзавот-полиз", locale=lang),
            callback_data=Factories.FaoliyatTuri(id=3).pack(),
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text=_("Сабзавот-ғалла", locale=lang),
            callback_data=Factories.FaoliyatTuri(id=4).pack(),
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text=_("Бошқа йўналиш", locale=lang),
            callback_data=Factories.FaoliyatTuri(id=5).pack(),
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text=_("🔙 Орқага", locale=lang),
            callback_data=Factories.Back(id="back").pack(),
        )
    )

    keyboard.adjust(1)
    return keyboard.as_markup()


async def download_cert(lang):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text=_("Сертификатни юклаб олиш", locale=lang),
            callback_data=Factories.Certificate(id="download").pack(),
        )
    )
    keyboard.adjust(1)

    return keyboard.as_markup()


async def region_inline_keyboard(lang, need_i_back = True):
    regions_list = await api.get_region_with_districts(lang)
    keyb = InlineKeyboardBuilder()
    for i in regions_list["data"]:
        keyb.add(
            InlineKeyboardButton(
                text=str(i["name"]),
                callback_data=Factories.Region(id=str(i["id"])).pack(),
            )
        )
    keyb.adjust(2)
    if need_i_back:
        keyb.row(
            InlineKeyboardButton(
                text=_("🔙 Орқага", locale=lang),
                callback_data=Factories.Back(id="back").pack(),
            )
        )

    return keyb.as_markup()


async def district_inline_keyboard(region_id, lang):
    districts_list = await api.get_region_with_districts(lang)
    keyb = InlineKeyboardBuilder()
    for i in districts_list["data"]:
        if str(i["id"]) == str(region_id):
            for j in i["districts"]:
                keyb.add(
                    InlineKeyboardButton(
                        text=str(j["name"]),
                        callback_data=Factories.District(id=str(j["id"])).pack(),
                    )
                )
    keyb.adjust(2)
    keyb.row(
        InlineKeyboardButton(
            text=_("🔙 Орқага", locale=lang),
            callback_data=Factories.Back(id="back").pack(),
        )
    )

    return keyb.as_markup()


async def channels_keyboard(lang):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text=_("Сувчилар Мактаби канали", locale=lang),
            url="https://t.me/suvchilar_maktabi",
        )
    )

    keyboard.row(
        InlineKeyboardButton(
            text=_("Обунани текшириш", locale=lang),
            callback_data=Factories.Language(language="check").pack(),
        )
    )

    return keyboard.as_markup()


async def score_keyboard(step, lang):
    keyboard = InlineKeyboardBuilder()
    step = str(step)
    keyboard.add(
        InlineKeyboardButton(
            text=_("1 (ёмон 😢)", locale=lang), callback_data=Factories.Score(id="1", step=step, emoji="1 (yomon😢)").pack()
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text=_("2 (қониқарсиз 🙁)", locale=lang), callback_data=Factories.Score(id="2", step=step, emoji="2 (qoniqarsiz🙁)").pack()
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text=_("3 (қониқарли 😐)", locale=lang), callback_data=Factories.Score(id="3", step=step, emoji="3 (qoniqarli 😐) ").pack()
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text=_("4 (яхши 🙂)", locale=lang), callback_data=Factories.Score(id="4", step=step, emoji="4 (yaxshi 🙂)").pack()
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text=_("5 (аъло 😀)", locale=lang), callback_data=Factories.Score(id="5", step=step, emoji="5 (a’lo 😀)").pack()
        )
    )
    keyboard.adjust(1)
    return keyboard.as_markup()


async def continue_step(lang):
    ke, locale=langyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(
            text=_("Давом этиш", locale=lang),
            callback_data="continue",
        )
    )

    return keyboard.as_markup()


class Factories:
    class Language(CallbackData, prefix="language"):
        language: str

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

    class Back(CallbackData, prefix="back"):
        id: str

    class Score(CallbackData, prefix="score"):
        id: str
        step: str
        emoji: str
