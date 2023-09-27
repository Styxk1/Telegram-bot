from aiogram import types
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from time import sleep
from datetime import datetime

from .keyboard import menu
from .run import bot, dp
from .command import flip, choise
from config.message import greetings, help, command_list
from config.config import id_admin
from config.config import id_admin
from games.tictactoe.launch import start_game
from database.database import (
    sql_start,
    sql_stop,
    exists,
    add_user,
    add_schedule,
    view_schedule,
    check_schedule,
    clear_schedule,
    add_choise,
)


async def send_to_adm_su(dp):
    sql_start()
    await bot.send_message(chat_id=id_admin, text="Bot is running")


async def send_to_adm_sd(dp):
    sql_stop()
    await bot.send_message(chat_id=id_admin, text="Bot disable")


async def check_time(dp):
    now = datetime.now()
    curr_time = now.strftime("%H:%M")
    data = check_schedule(curr_time)
    if len(data[0]) > 0:
        for i in range(len(data) - 1):
            st = "Пришло время для ваших планов:\n" + str(data[1][i])
            await bot.send_message(chat_id=data[0][i], text=st)
    if curr_time == "00:00":
        clear_schedule()
        await bot.send_message(chat_id=id_admin, text="Произведена очистка расписания.")


@dp.message_handler(Command("start"))
async def command_start_handler(message: Message):
    if exists(message.from_user.id):
        await message.answer(
            f"Привет, {message.from_user.first_name}!\nЧтобы увидеть все команды напиши:\n/command",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await message.answer(greetings)
        await command_dating_handler(message)


@dp.message_handler(Command("troll"))
async def command_troll_matvey(message: Message):
    print("START TROLLING XDDDDD")
    while True:
        await bot.send_message(chat_id=1203067039, text="LOH")


@dp.message_handler(Command("command"))
async def command_list_handler(message: Message):
    await message.answer(command_list)


@dp.message_handler(Command("flip"))
async def command_flip_handler(message: Message):
    await message.answer("Подбрасываем монетку!", reply_markup=ReplyKeyboardRemove())
    sleep(0.5)
    await message.answer("Ловим и смотрим результат!")
    sleep(1)
    await message.answer("...")
    sleep(0.5)
    st = flip()
    await message.answer(st)


class Choise_state(StatesGroup):
    text = State()


@dp.message_handler(Command("choice"))
async def command_choise_handler(message: Message):
    await message.answer(
        "Постараюсь помочь тебе сделать выбор!\n\nПиши из чего ты делаешь выбор, "
        "я все проанализирую и выберу лучшее и возможного!\n(Когда закончишь вводить отправь 0,"
        "чтобы я понял что могу начинать выбирать)"
    )
    await Choise_state.text.set()


@dp.message_handler(state=Choise_state.text)
async def get_text1(message: Message, state: FSMContext):
    if message.text != "0":
        add_choise(message.from_user.id, message.text)
        await Choise_state.text.set()
    else:
        await state.finish()
        st = choise(message.from_user.id)
        await message.answer(f"Я думаю лучше всего будет:\n{st}")
        print(st)


@dp.message_handler(Command("help"))
async def command_help_handler(message: Message):
    await message.answer(help, reply_markup=ReplyKeyboardRemove())


@dp.message_handler(Command("menu"))
async def command_menu_handler(message: Message):
    await message.answer("Выбери команду.", reply_markup=menu)


class Dating(StatesGroup):
    name = State()
    age = State()


@dp.message_handler(Command("dating"))
async def command_dating_handler(message: Message):
    if exists(message.from_user.id):
        await message.answer(
            "Привет!\nМы уже знакомы!", reply_markup=ReplyKeyboardRemove()
        )
    else:
        await message.answer("Как тебя зовут?", reply_markup=ReplyKeyboardRemove())
        await Dating.name.set()


@dp.message_handler(state=Dating.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer("Отлично!\nТепер скажи, сколько тебе лет?")
    await Dating.next()


@dp.message_handler(state=Dating.age)
async def get_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    data = await state.get_data()
    add_user(message.from_user.id, data["username"], data["age"])
    await message.answer(
        (f"Тебя зовут: {data['username']};\n" f"Твой возраст: {data['age']}!")
    )
    await state.finish()


class Schedule(StatesGroup):
    action = State()
    time = State()


@dp.message_handler(Command("schedule_add"))
async def command_schedule_add_handler(message: Message):
    await message.answer(
        """Какой план необходимо добавить в твой график?\n
        (График работает только на остаток текущего дня, очистка событий происходит в 00:00""",
        reply_markup=ReplyKeyboardRemove(),
    )
    await Schedule.action.set()


@dp.message_handler(state=Schedule.action)
async def get_action(message: Message, state: FSMContext):
    await state.update_data(action=message.text)
    await message.answer(
        "Отлично!\nТепер скажи, во сколько мне напомнить тебе про это?\n(Время напиши в формате HH:MM)"
    )
    await Schedule.next()


@dp.message_handler(state=Schedule.time)
async def get_time(message: Message, state: FSMContext):
    await state.update_data(time=message.text)
    data = await state.get_data()
    if add_schedule(message.from_user.id, data["action"], data["time"]) == 0:
        await message.answer("Сначала нужно познакомиться!\n/start")
    await message.answer("Обязательно напомню когда придет время!")
    await state.finish()


@dp.message_handler(Command("schedule_view"))
async def command_schedule_view_handler(message: Message):
    data = view_schedule(message.from_user.id)
    if data == None:
        await message.answer("Сначала нужно познакомиться!\n/start")
    if len(data) == 0:
        await message.answer(
            "Похоже что вы еще ничего не планировали!\nСделать это можно с помощью команды:\n/schedule_add",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        now = datetime.now()
        curr_time = now.strftime("%H:%M")
        bold = True
        st = ""
        for i in range(len(data[0])):
            if curr_time > data[0][i]:
                st = (
                    st
                    + "<strike>"
                    + data[0][i]
                    + " - "
                    + data[1][i]
                    + "</strike>"
                    + "\n"
                )
            elif bold:
                st = st + "<b>" + data[0][i] + " - " + data[1][i] + "</b>" + "\n"
                bold = False
            else:
                st = st + data[0][i] + " - " + data[1][i] + "\n"
        await message.answer("Список ваших планов:", reply_markup=ReplyKeyboardRemove())
        await message.answer(st, parse_mode=types.ParseMode.HTML)


@dp.message_handler(
    Text(
        equals=[
            "Приветственное сообщение",
            "Список команд",
            "Подбросить монетку",
            "Сделать выбор",
            "Познакомиться",
            "Добавить пункт в график",
            "Показать график",
            "Помощь",
        ]
    )
)
async def get_menu_command(message: Message):
    menu_dictionary = {
        "Приветственное сообщение": command_start_handler,
        "Список команд": command_list_handler,
        "Подбросить монетку": command_flip_handler,
        "Сделать выбор": command_choise_handler,
        "Познакомиться": command_dating_handler,
        "Добавить пункт в график": command_schedule_add_handler,
        "Показать график": command_schedule_view_handler,
        "Помощь": command_help_handler,
    }
    await menu_dictionary[message.text]((message))


@dp.message_handler(Command("play"))
async def command_start_play_tictactoe(message: Message):
    await start_game(message)


@dp.message_handler()
async def echo(message: Message):
    text = f"Hi, you write: {message.text}"
    await message.answer(text=text)
