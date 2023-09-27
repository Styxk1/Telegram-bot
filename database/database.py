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

    try:
        cur.execute("SELECT * FROM choise")

    except sqlite3.OperationalError:
        print("Database choise does not exsist")
        if sqlite3.OperationalError:
            cur.execute(
                """CREATE TABLE choise(
                        id INTEGER PRIMARY KEY,
                        tg_id BIGINT,
                        option text
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
    if user_id == 0:
        return 0
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
    cur.execute("SELECT COUNT(*) FROM schedule")
    temp = cur.fetchall()[0]
    if temp[0] == 0:
        return []
    else:
        user_id = get_id(id)
        if user_id == None:
            return None
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


def add_choise(id, text):
    cur.execute("INSERT INTO choise (tg_id, option) VALUES(?,?)", (id, text))
    conn.commit()
    print("Добавлена опция в выбор")


def get_choise(id):
    data = []
    cur.execute("SELECT option FROM choise WHERE tg_id = (?)", (id,))
    temp = cur.fetchall()
    for i in temp:
        data.append(i[0])
    clear_choise(id)
    return data


def clear_choise(id):
    cur.execute("DELETE FROM choise WHERE tg_id = (?)", (id,))
    conn.commit()
    print(f"Очищена таблица choise пользователя: {id}")


def get_id(id):
    print(id)
    cur.execute("SELECT EXISTS(SELECT * FROM users WHERE tg_id = (?))", (id,))
    temp = cur.fetchone()[0]
    print(temp)
    if temp == 0:
        return None
    else:
        return temp


def get_name_from_db(id):
    print(id)
    data = [[], []]
    cur.execute("SELECT tg_id, name FROM users WHERE tg_id != (?)", (id,))
    temp = cur.fetchall()
    for i in temp:
        data[0].append(i[0])
        data[1].append(i[1])
    return data


def sql_stop():
    print("Закрываем БД")
    conn.close()
