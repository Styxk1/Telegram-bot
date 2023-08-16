from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="/flip"),
            KeyboardButton(text="/choice"),
        ],
        [
            KeyboardButton(text="/help")
        ]
    ]
)