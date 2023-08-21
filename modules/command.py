from random import randint
from aiogram.types import Message


def flip():
    num = randint(1, 2)
    if num == 1:
        return "Выпала решка!"
    else:
        return "Выпал орел!"


def choise(arr):
    rn = randint(0, len(arr))
    return arr[rn]
