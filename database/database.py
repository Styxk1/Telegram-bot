import sqlite3

conn = sqlite3.connect("database/database.db")
cur = conn.cursor()


def check_db():
    try:
        cur.execute("SELECT * FROM users")

    except sqlite3.OperationalError:
        print("Database users does not exsist")
        if sqlite3.OperationalError:
            cur.execute(
                """CREATE TABLE users(
                        id INTEGER PRIMARY KEY,
                        tg_id BIGINT,
                        name text,
                        age INTEGER
            )"""
            )
            conn.commit()

    try:
        cur.execute("SELECT * FROM schedule")

    except sqlite3.OperationalError:
        print("Database schedule does not exsist")
        if sqlite3.OperationalError:
            cur.execute(
                """CREATE TABLE schedule(
                        id INTEGER PRIMARY KEY,
                        reminder_time TIME,
                        action text,
                        user_id BIGINT,
                        FOREIGN KEY (user_id) REFERENCES users(id)
            )"""
            )
            conn.commit()


def sql_start():
    check_db()
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


def add_user(
    id,
    name,
    age,
):
    cur.execute("INSERT INTO users (tg_id, name, age) VALUES(?, ?, ?)", (id, name, age))
    conn.commit()
    print("Добавлен новый пользователь")


def add_schedule(id, action, time):
    user_id = get_id(id)
    cur.execute(
        "INSERT INTO schedule (reminder_time, action, user_id) VALUES(?, ?, ?)",
        (time, action, user_id),
    )
    conn.commit()
    print("Добавлен новый пункт в расписании")


def check_schedule(time):
    data = [[], []]
    cur.execute("SELECT action FROM schedule WHERE reminder_time = (?)", (time,))
    temp = cur.fetchall()
    for i in temp:
        data[1].append(i[0])
    cur.execute(
        "SELECT tg_id FROM users U JOIN schedule S on U.id = S.user_id WHERE reminder_time = (?)",
        (time,),
    )
    temp = cur.fetchall()
    for i in temp:
        data[0].append(i[0])
    return data


def view_schedule(id):
    user_id = get_id(id)
    data = [[], []]
    cur.execute(
        "SELECT reminder_time FROM schedule WHERE user_id = (?) ORDER BY reminder_time",
        (user_id,),
    )
    temp = cur.fetchall()
    for i in temp:
        data[0].append(i[0])
    cur.execute(
        "SELECT action FROM schedule WHERE user_id = (?) ORDER BY reminder_time",
        (user_id,),
    )
    temp = cur.fetchall()
    for i in temp:
        data[1].append(i[0])
    return data


def clear_schedule():
    cur.execute("DELETE FROM schedule")
    conn.commit()


def get_id(id):
    print(id)
    cur.execute("SELECT id FROM users WHERE tg_id = (?)", (id,))
    return cur.fetchone()[0]


def sql_stop():
    print("Закрываем БД")
    conn.close()
