def update_field(field, x, y, ch):
    x_cord = int(x)
    y_cord = int(y)
    cord_str = 3 * x_cord + y_cord
    list_str = list(field)
    if ch == "X":
        list_str[cord_str] = "1"
    else:
        list_str[cord_str] = "2"
    field = "".join(list_str)
    return field


def check_occupied(field, x, y):
    x_cord = int(x)
    y_cord = int(y)
    cord_str = 3 * x_cord + y_cord
    list_str = list(field)
    if list_str[cord_str] != "0":
        return True
    return False


def check_full(field):
    list_str = list(field)
    count = 0
    for i in range(len(list_str)):
        if list_str[i] != "0":
            count += 1
    if count == 9:
        return True
    else:
        return False


def view_field(field):
    st = "Игровое поле:\n\n"
    for i in range(3):
        for j in range(3):
            cord_str = 3 * i + j
            if field[cord_str] == "0":
                st += "     "
            elif field[cord_str] == "1":
                st += " X "
            else:
                st += " 0 "
            if j < 2:
                st += "|"
        if i < 2:
            st += "\n----------------\n"
    return st


def check_for_win(field):
    list_str = list(field)
    print(list_str)
    # Проверка горизонталей
    for i in range(3):
        count_x = 0
        count_y = 0
        for j in range(3):
            cord = 3 * (i) + j
            if list_str[cord] == "1":
                count_x += 1
            if list_str[cord] == "2":
                count_y += 1
        if count_x == 3 or count_y == 3:
            return True
    # Проверка вертикалей
    for i in range(3):
        count_x = 0
        count_y = 0
        for j in range(3):
            cord = i + 3 * j
            if list_str[cord] == "1":
                count_x += 1
            if list_str[cord] == "2":
                count_y += 1
        if count_x == 3 or count_y == 3:
            return True
    # Проверка диагоналей
    for i in range(2):
        count_y = 0
        count_x = 0
        for j in range(3):
            if i == 0:
                cord = 0 + 4 * j
            else:
                cord = 2 + 2 * j
            if list_str[cord] == "1":
                count_x += 1
            if list_str[cord] == "2":
                count_y += 1
        if count_x == 3 or count_y == 3:
            return True
    return False
