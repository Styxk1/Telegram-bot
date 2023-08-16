from aiogram.dispatcher import FSMContext
from main import bot, dp
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from message import greetings, help
from time import sleep
from command import flip, choise
from keyboard import menu
from config import id_admin
from database import sql_start, sql_stop
from database import exists, add_user


async def send_to_adm_su(dp):
    sql_start()
    await bot.send_message(chat_id=id_admin, text="Bot is running")


async def send_to_adm_sd(dp):
    sql_stop()
    await bot.send_message(chat_id=id_admin, text="Bot disable")


@dp.message_handler(Command("start"))
async def command_start_handler(message: Message):
    await message.answer(greetings)
    
    


@dp.message_handler(Command("flip"))
async def command_flip_handler(message: Message):
    await message.answer("Подбрасываем монетку!", reply_markup=ReplyKeyboardRemove())
    sleep(0.5)
    await message.answer("Ловим и смотрим результат!")
    sleep(0.5)
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


class MyDialog(StatesGroup):
    name = State()
    age = State()


@dp.message_handler(Command("dating"))
async def command_dating_handler(message: Message):
    if exists(message.from_user.id):
        await message.answer("Привет!")
    else:
        await message.answer("Похоже Вы здесь впервые!\nДавайте знакомиться!")
        await message.answer("Как тебя зовут?")
        await MyDialog.name.set()


@dp.message_handler(state=MyDialog.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer("Отлично!\nТепер скажи, сколько тебе лет?")
    await MyDialog.next()

@dp.message_handler(state=MyDialog.age)
async def get_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    data = await state.get_data()
    add_user(message.from_user.id, data["username"], data["age"])
    await message.answer((f"Тебя зовут: {data['username']};\n"
                          f"Твой возраст: {data['age']}!"))
    await state.finish()

@dp.message_handler(Text(equals=["Test1", "Test2", "Test3"]))
async def get_menu_command(message: Message):
    await message.answer(f"Вы выбрали {message.text}.", reply_markup=ReplyKeyboardRemove())


@dp.message_handler()
async def echo(message: Message):
    text = f"Hi, you write: {message.text}"
    await message.answer(text=text)