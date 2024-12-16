n = int(input())  # Максимальное возможное число
possible_numbers = set(range(1, n + 1))  # Все возможные числа
print(possible_numbers)
while True:
    query = input().strip()  # Ввод запроса или HELP
    if query == "HELP":
        break
    query_set = set(map(int, query.split()))  # Преобразуем запрос в множество

    # Логика ответа
    if len(query_set) <= len(possible_numbers) / 2:  #
        print("NO")
        possible_numbers -= query_set  # Исключаем эти числа
        print(possible_numbers)
    else:  #
        print("YES")
        possible_numbers &= query_set  # Пересекаем множество
        print(possible_numbers)

# Вывод оставшихся чисел в порядке возрастания
print(" ".join(map(str, sorted(possible_numbers))))
