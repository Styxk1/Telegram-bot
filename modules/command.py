from random import randint

from database.database import get_choise


def flip():
    num = randint(1, 2)
    if num == 1:
        return "Выпала решка!"
    else:
        return "Выпал орел!"


def choise(id):
    arr = get_choise(id)
    print(arr)
    rn = randint(0, len(arr) - 1)
    return arr[rn]
