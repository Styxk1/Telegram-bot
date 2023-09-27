from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from config.message import empty_base
from modules.run import bot, dp
from database.database import get_name_from_db
from .game import game


async def get_name_to_keyboard(message: Message):
    button = InlineKeyboardMarkup(row_width=1)
    data = get_name_from_db(message.from_user.id)
    if len(data) == 0:
        return 0
    else:
        for i in range(len(data)):
            temp = InlineKeyboardButton(
                text=data[1][i], callback_data=f"id_{data[0][i]}"
            )
            button.add(temp)
        return button


async def start_game(message: Message):
    button = await get_name_to_keyboard(message)
    if button == 0:
        await message.answer(empty_base)
    else:
        await message.answer("Выбери соперника:", reply_markup=button)


@dp.callback_query_handler(text_startswith="id_")
async def choise_opponent(call: types.CallbackQuery):
    await bot.delete_message(
        chat_id=call.from_user.id, message_id=call.message.message_id
    )
    await bot.send_message(
        chat_id=call.from_user.id,
        text="Отправили сообщение пользователю о вашем вызове!\nОжидание его ответа...",
    )
    id_opponent = call.data.split("_")[1]
    await user_answer(id_opponent, call.from_user.id)


async def user_answer(id_opponent, id):
    button = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton(
        text="Да", callback_data=f"accept_True_{id}_{id_opponent}"
    )
    button2 = InlineKeyboardButton(text="Нет", callback_data=f"accept_False")
    button.add(button1, button2)
    await bot.send_message(
        chat_id=id_opponent,
        text="Вам бросили вызов в игре Крестики нолики!\nПринимаете вызов?",
        reply_markup=button,
    )


@dp.callback_query_handler(text_startswith="accept_")
async def opponent_accept(call: types.CallbackQuery):
    await bot.delete_message(
        chat_id=call.from_user.id, message_id=call.message.message_id
    )
    accept = call.data.split("_")[1]
    if accept == "False":
        await bot.send_message(
            chat_id=call.from_user.id,
            text="Вы отказались.",
        )
    else:
        id = call.data.split("_")[2]
        id_opponent = call.data.split("_")[3]
        await bot.send_message(
            chat_id=call.from_user.id,
            text="Вы приняли вызов!\n\nНачинаем игру!",
        )
        await game(id, id_opponent)
