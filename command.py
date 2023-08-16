from random import randint
from aiogram.types import Message


def flip():
    num = randint(1, 2)
    if num == 1:
        return "Выпала решка!"
    else:
        return "Выпал орел!"

def choise():
    arr = []
    work = True
    while work:
        temp = " "
        print(temp)
        if temp == "0":
            work = False
        else:
            arr.append(temp)
    num = randint(0, len(arr))
    return arr[num]