#LAB 4 Дука Виталий 39.2 вариант 9
def task9(arr):
    """Найти элементы перед последним минимальным."""
    if len(arr) < 2:
        return []
    min_value = min(arr)
    last_min_index = len(arr) - 1 - arr[::-1].index(min_value)
    return arr[:last_min_index] if last_min_index > 0 else []


def task21(arr):
    """Найти элементы после первого максимального."""
    if len(arr) < 2:
        return []
    max_value = max(arr)
    first_max_index = arr.index(max_value)
    return arr[first_max_index + 1:]


def task33(arr):
    """Проверить, чередуются ли положительные и отрицательные числа."""
    for i in range(len(arr) - 1):
        if (arr[i] > 0 and arr[i + 1] > 0) or (arr[i] < 0 and arr[i + 1] < 0):
            return False
    return True


def task45(arr, a, b):
    array = arr
    sum = 0
    for i in range(len(array) - 1):
        if (i >= a and i <= b):
            sum = sum + arr[i]
    return sum


def task57(arr):
    """Найти количество элементов, которые больше суммы всех предыдущих."""
    result = []
    current_sum = 0
    for num in arr:
        if num > current_sum:
            result.append(num)
        current_sum += num
    return len(result)


def input_massiv():
    """Получить массив от пользователя."""
    return list(map(int, input("Введите элементы массива через пробел: ").split()))


while True:
    print("\nВыберите задачу для решения:")
    print("1. Задача 9: Найти элементы перед последним минимальным.")
    print("2. Задача 21: Найти элементы после первого максимального.")
    print("3. Задача 33: Проверить чередование положительных и отрицательных.")
    print("4. Задача 45: Найти сумму элементов в интервале.")
    print("5. Задача 57: Найти элементы, которые больше суммы всех предыдущих.")
    print("6. Выйти из программы.")

    choice = input("Задача: ")

    if choice == '6':
        print("Выход из программы.")
        break

    arr = input_massiv()

    if choice == '1':
        result = task9(arr)
        print("Результат:", result)
    elif choice == '2':
        result = task21(arr)
        print("Результат:", result)
    elif choice == '3':
        result = task33(arr)
        print("Чередуются положительные и отрицательные числа:", result)
    elif choice == '4':
        a = int(input("Введите значение a: "))
        b = int(input("Введите значение b: "))
        result = task45(arr, a, b)
        print("Сумма элементов в интервале [{}, {}]: {}".format(a, b, result))
    elif choice == '5':
        result = task57(arr)
        print("Элементы, которые больше суммы всех предыдущих:", result)
    else:
        print("Неверный выбор, попробуйте снова.")
