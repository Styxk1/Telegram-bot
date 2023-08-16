import sqlite3

from main import bot
from aiogram.types import Message

conn = sqlite3.connect('users.db')
cur = conn.cursor()

def sql_start():
    if conn:
        print("Успешное подключение к БД")
    else:
        print("Ошибка при подключении к БД")

def exists(id):
    cur.execute("SELECT * FROM users")
    temp = cur.fetchall()
    print(temp)
    cur.execute("SELECT tg_id FROM users")
    bd = cur.fetchall()
    print(bd)
    print(id)
    if id not in bd:
        return False
    else:
        return True

def add_user(id, name, age,):
    cur.execute("INSERT INTO users (tg_id, name, age) VALUES(?, ?, ?)",
                (id, name, age))
    conn.commit()
    print("Добавлен новый пользователь")

def sql_stop():
    print("Закрываем БД")
    conn.close()