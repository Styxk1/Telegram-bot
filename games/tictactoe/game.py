from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from modules.run import bot, dp
from .field import *


async def game(id_first, id_second):
    field = "000000000"
    await step("X", id_first, id_second, field)


async def step(ch, id, id_opponent, field):
    button = InlineKeyboardMarkup(row_width=1)
    for i in range(3):
        if ch == "X":
            mark = "X"
        elif ch == "Y":
            mark = "0"
        button1 = InlineKeyboardButton(
            text=f"<strike>{mark}</strike>",
            callback_data=f"step_{ch}_{i}_0_{id}_{id_opponent}_{field}",
            parse_mode=types.ParseMode.HTML,
        )
        button2 = InlineKeyboardButton(
            text=f"{mark}",
            callback_data=f"step_{ch}_{i}_1_{id}_{id_opponent}_{field}",
            parse_mode=types.ParseMode.HTML,
        )
        button3 = InlineKeyboardButton(
            text=f"{mark}",
            callback_data=f"step_{ch}_{i}_2_{id}_{id_opponent}_{field}",
            parse_mode=types.ParseMode.HTML,
        )
        button.row(button1, button2, button3)
    st = view_field(field)
    await bot.send_message(
        chat_id=id, text=st, reply_markup=button, parse_mode=types.ParseMode.HTML
    )


async def end_game(id, id_opponent, win):
    if win:
        st_win = f"Игра закончена!\n\nВы победили!"
        await bot.send_message(chat_id=id, text=st_win)
        st_lose = f"Игра закончена!\n\nК сожалению вы проиграли :("
        await bot.send_message(chat_id=id_opponent, text=st_lose)
    else:
        st_draw = "Игра закончена!\n\nНичья!"
        await bot.send_message(chat_id=id, text=st_draw)
        await bot.send_message(chat_id=id_opponent, text=st_draw)


@dp.callback_query_handler(text_startswith="step_")
async def process(call: types.CallbackQuery):
    await bot.delete_message(
        chat_id=call.from_user.id, message_id=call.message.message_id
    )
    ch = call.data.split("_")[1]
    x = call.data.split("_")[2]
    y = call.data.split("_")[3]
    id = call.data.split("_")[4]
    id_opponent = call.data.split("_")[5]
    field = call.data.split("_")[6]
    if check_occupied(field, x, y):
        await bot.send_message(
            chat_id=call.from_user.id,
            text="Выбранная вами клетка занята!\nВыберете другую.",
        )
        await step(ch, id, id_opponent, field)
    else:
        field = update_field(field, x, y, ch)
        if check_for_win(field):
            await end_game(id, id_opponent, True)
        else:
            if check_full(field):
                await end_game(id, id_opponent, False)
            else:
                if ch == "X":
                    await step("Y", id_opponent, id, field)
                else:
                    await step("X", id_opponent, id, field)
