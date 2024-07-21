from aiogram import F, types, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, or_f
from aiogram.utils.formatting import (
    as_list,
    as_marked_section,
    Bold,
)

from database.orm_query import orm_get_products
from filters.chat_types import ChatTypeFilter

from kbds.reply import get_keyboard

from sqlalchemy.ext.asyncio import AsyncSession

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(
        "Привет, я виртуальный помощник",
        reply_markup=get_keyboard(
            "Меню",
            "О нас",
            "Варианты оплаты",
            "Варианты доставки",
            "Обратная связь",
            placeholder="Что вас интересует?",
            sizes=(2, 2, 1)
        ),
    )


@user_private_router.message(or_f(Command("menu"), (F.text.lower() == "меню")))
async def menu_cmd(message: types.Message, session: AsyncSession):
    for product in await orm_get_products(session):
        await message.answer_photo(
            product.image,
            caption=f"<strong>{product.name}\
                    </strong>\n{product.description}\n Стоимость: {round(product.price, 2)}",
        )
    await message.answer("Вот меню ⬆️")


@user_private_router.message(F.text.lower() == "о нас")
@user_private_router.message(Command("about"))
async def about_cmd(message: types.Message):
    await message.answer('Образовательный телеграм бот, для теста и дапьнейшего развития для портфолио. Данный бот был сойдан на фрейворке iaogram 3.')


@user_private_router.message(F.text.lower() == "варианты оплаты")
@user_private_router.message(Command("payment"))
async def payment_cmd(message: types.Message):
    text = as_marked_section(
        Bold("Варианты оплаты:"),
        "Картой в боте",
        "При получении карта/кеш",
        "В заведении",
        marker="✅ ",
    )
    await message.answer(text.as_html())


@user_private_router.message(
    (F.text.lower().contains("доставк")) | (F.text.lower() == "варианты доставки"))
@user_private_router.message(Command("shipping"))
async def menu_cmd(message: types.Message):
    text = as_list(
        as_marked_section(
            Bold("Варианты доставки/заказа:"),
            "Курьер",
            "Самовынос (сейчас прибегу заберу)",
            "Покушаю у Вас (сейчас прибегу)",
            marker="✅ ",
        ),
        as_marked_section(
            Bold("Нельзя:"),
            "Почта",
            "Голуби",
            marker="❌ "
        ),
        sep="\n----------------------\n",
    )
    await message.answer(text.as_html())


@user_private_router.message(F.text.lower() == "обратная связь")
async def call_cmd(message: types.Message):
    await message.answer("Вдруг возникнет вопрос, а как связаться с создателем бота в целях сотруднечества, так вот: enoitim067@gmail.com")