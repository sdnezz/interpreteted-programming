# Вариант: ((8 - 1) %10 +1 ) , где 8 – номер по списку.
# Дука Виталий 39.2 лаб 8
import re

def is_valid_username(username):
    # Проверка длины
    if not (3 <= len(username) <= 15):
        return False
    # Проверка разрешенных символов и позиции подчеркиваний и тире
    pattern = r'^[A-ZА-Яa-zа-я0-9][A-ZА-Яa-zа-я0-9_-]*[A-ZА-Яa-zа-я0-9]$'
    return bool(re.match(pattern, username))

def get_username(username):
    # Проверка валидности имени и выброс исключения при некорректном аргументе
    if not is_valid_username(username):
        raise ValueError("Некорректное имя пользователя")
    return username

# Ввод имени пользователя с клавиатуры
try:
    user_name = input("Введите имя пользователя: ")
    valid_username = get_username(user_name)
    print("Имя пользователя корректно:", valid_username)
except ValueError as e:
    print(e)
