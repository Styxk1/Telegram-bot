from aiogram.dispatcher import FSMContext
from main import bot, dp
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from message import greetings, help, command_list
from time import sleep
from command import flip, choise
from keyboard import menu
from config import id_admin
from database import sql_start, sql_stop
from database import exists, add_user, add_schedule, view_schedule
from datetime import datetime


async def send_to_adm_su(dp):
    sql_start()
    await bot.send_message(chat_id=id_admin, text="Bot is running")


async def send_to_adm_sd(dp):
    sql_stop()
    await bot.send_message(chat_id=id_admin, text="Bot disable")

async def check_time(dp):
    now = datetime.now()
    curr_time = now.strftime("%H:%M")
    print(curr_time)

@dp.message_handler(Command("start"))
async def command_start_handler(message: Message):
    if exists(message.from_user.id):
        await message.answer(f"Привет, {message.from_user.first_name}!\nЧтобы увидеть все команды напиши:\n/command")
    else:
        await message.answer(greetings)
        await command_dating_handler(message)


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
    sleep(1)
    st = flip()
    await message.answer(st)


@dp.message_handler(Command("choice"))
async def command_choise_handler(message: Message):
    await message.answer("На доработке.")
    '''
    await message.answer("Постараюсь помочь тебе сделать выбор!\n\n Пиши из чего ты делаешь выбор, "
                         "я все проанализирую и выберу лучшее и возможного!\n(Когда закончишь вводить отправь 0,"
                         "чтобы я понял что могу начинать выбирать)")
    st = choise()
    await message.answer("Я думаю что...")
    sleep(0.5)
    await message.answer("Лучшее из всего это...")
    sleep(1)
    await message.answer(st)
    '''


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
        await message.answer("Привет!\n Мы уже знакомы!")
    else:
        await message.answer("Как тебя зовут?")
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
    await message.answer((f"Тебя зовут: {data['username']};\n"
                          f"Твой возраст: {data['age']}!"))
    await state.finish()

class Schedule(StatesGroup):
    action = State()
    time = State()

@dp.message_handler(Command("schedule_add"))
async def command_schedule_add_handler(message: Message):
    await message.answer("Какой план необходимо добавить в твой график?")
    await Schedule.action.set()

@dp.message_handler(state=Schedule.action)
async def get_action(message: Message, state: FSMContext):
    await state.update_data(act=message.text)
    await message.answer("Отлично!\nТепер скажи, во сколько мне напомнить тебе про это?")
    await Schedule.next()

@dp.message_handler(state=Schedule.time)
async def get_time(message: Message, state: FSMContext):
    await state.update_data(time=message.text)
    data = await state.get_data()
    add_schedule(message.from_user.id, data["act"], data["time"])
    await message.answer("Обязательно напомню когда придет время!")
    await state.finish()

@dp.message_handler(Command("schedule_view"))
async def command_schedule_view_handler(message: Message):
    data = view_schedule(message.from_user.id)
    if len(data) == 0:
        await message.answer("Похоже что вы еще ничего не планировали!\nСделать это можно с помощью команды:\n/schedule_add")
    else:
        await message.answer(data)

@dp.message_handler(Text(equals=["Test1", "Test2", "Test3"]))
async def get_menu_command(message: Message):
    await message.answer(f"Вы выбрали {message.text}.", reply_markup=ReplyKeyboardRemove())


@dp.message_handler()
async def echo(message: Message):
    text = f"Hi, you write: {message.text}"
    await message.answer(text=text)