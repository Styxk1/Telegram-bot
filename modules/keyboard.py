from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Приветственное сообщение"),
        ],
        [
            KeyboardButton(text="Список команд"),
            KeyboardButton(text="Подбросить монетку"),
        ],
        [
            KeyboardButton(text="Меню"),
            KeyboardButton(text="Познакомиться"),
        ],
        [
            KeyboardButton(text="Добавить пункт в график"),
            KeyboardButton(text="Показать график"),
        ],
        [KeyboardButton(text="Помощь")],
    ],
)
