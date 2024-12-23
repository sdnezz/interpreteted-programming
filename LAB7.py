def read_input(file_path):
    with open(file_path, 'r') as f:
        # Чтение первой строки - основные параметры
        n, k, v, m = map(int, f.readline().strip().split())

        # Чтение данных о домах
        houses = []
        for line in f:
            position, mail_weight = map(int, line.strip().split())
            houses.append((position, mail_weight))

    return n, k, v, m, houses


def calculate_packages(mail_weight, max_weight):
    """Функция для расчета необходимого количества пакетов для доставки"""
    return (mail_weight + max_weight - 1) // max_weight  # округляем вверх


def optimal_post_office(n, k, v, m, houses):
    max_deliverable_packages = 0
    best_position = None
    best_deliverable_houses = []
    best_undeliverable_houses = []

    # Перебираем каждый дом как потенциальное местоположение почтового отделения
    for i in range(len(houses)):
        post_office_position = houses[i][0]
        deliverable_packages = 0
        deliverable_houses = []
        undeliverable_houses = []

        print(f"\nПроверка дома на позиции {post_office_position} как почтового отделения:")

        # Считаем количество пакетов для всех домов в пределах досягаемости
        for position, mail_weight in houses:
            # Рассчитываем минимальное расстояние с учетом кольцевой дороги
            distance = min(abs(position - post_office_position), k - abs(position - post_office_position))

            if distance <= m:
                # Если дом находится в зоне досягаемости, считаем количество пакетов
                required_packages = calculate_packages(mail_weight, v)
                deliverable_packages += required_packages
                deliverable_houses.append((position, required_packages))
                print(
                    f"  Дом на позиции {position}: {required_packages} пакетов (в зоне досягаемости, расстояние {distance})")
            else:
                # Дом недоступен для доставки
                undeliverable_houses.append(position)
                print(f"  Дом на позиции {position}: недоступен для доставки (расстояние {distance})")

        print(f"Всего доставлено пакетов из дома на позиции {post_office_position}: {deliverable_packages}")

        # Обновляем максимальное количество доставленных пакетов и лучшую позицию
        if deliverable_packages > max_deliverable_packages:
            max_deliverable_packages = deliverable_packages
            best_position = post_office_position
            best_deliverable_houses = deliverable_houses
            best_undeliverable_houses = undeliverable_houses

    # Вывод окончательного результата
    print("\nРезультат:")
    print(f"Оптимальное расположение почтового отделения: дом на позиции {best_position}")
    print(f"Максимальное количество доставляемых пакетов: {max_deliverable_packages}")
    print("Дома, в которые удалось доставить посылки:")
    for position, packages in best_deliverable_houses:
        print(f"  Позиция {position}: {packages} пакетов")
    print("Дома, в которые не удалось доставить посылки:")
    for position in best_undeliverable_houses:
        print(f"  Позиция {position}")

    return max_deliverable_packages


# Основной код
file_path = '27-124a.txt'  # Замените на ваш файл
n, k, v, m, houses = read_input(file_path)
result = optimal_post_office(n, k, v, m, houses)
print("Максимальное количество доставляемых пакетов:", result)
