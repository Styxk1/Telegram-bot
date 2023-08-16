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
    cur.execute("SELECT tg_id FROM users")
    bd = cur.fetchall()
    for i in bd:
        if id == i[0]:
            return True
    return False

def add_user(id, name, age,):
    cur.execute("INSERT INTO users (tg_id, name, age) VALUES(?, ?, ?)",
                (id, name, age))
    conn.commit()
    print("Добавлен новый пользователь")

def add_schedule(id, action, time):
    user_id = get_id(id)
    cur.execute("INSERT INTO schedule (reminder_time, action, user_id) VALUES(?, ?, ?)",
                (time, action, user_id))
    conn.commit()
    print("Добавлен новый пункт в расписании")

def view_schedule(id):
    user_id = get_id(id)
    cur.execute("SELECT action, reminder_time FROM schedule WHERE user_id = (?)", (user_id,))
    data = cur.fetchall()
    return data

def get_id(id):
    print(id)
    cur.execute("SELECT id FROM users WHERE tg_id = (?)", (id,))
    return cur.fetchone()[0]

def sql_stop():
    print("Закрываем БД")
    conn.close()