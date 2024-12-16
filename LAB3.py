from collections import Counter  # Импортируем Counter для подсчета частоты символов в тексте
#Лабораторная работа №3 Дука Виталий 39.2 (вариант 9)
# === Задача 3 ===
# Задача: найти разницу между частотой символов в тексте и их частотой в русском алфавите.
# Сортируем символы в порядке увеличения разницы.
def frequency_difference(text, alphabet_freq):
    text_freq = Counter(text)  # Подсчитываем частоту каждого символа в тексте
    differences = {}  # Создаем пустой словарь для хранения разницы частот
    for char, freq in text_freq.items():
        if char in alphabet_freq:  # Проверяем, есть ли символ в заданном алфавите
            # Разница между частотой символа в тексте и частотой в среднем алфавите
            differences[char] = abs(freq / len(text) - alphabet_freq[char])
    return sorted(differences.items(), key=lambda x: x[1])  # Сортируем символы по возрастанию разницы


# === Задача 5 ===
# Задача: найти квадратичное отклонение частоты наиболее часто встречаемого символа в тексте.
# Сравниваем частоту самого частого символа с усредненной частотой.
def quadratic_deviation(text):
    text_freq = Counter(text)  # Подсчитываем частоту символов в тексте
    # Находим самый часто встречающийся символ и его количество
    most_common_char, count = text_freq.most_common(1)[0]  # most_common возвращает [(символ, частота)]
    most_common_freq = count / len(text)  # Частота самого частого символа
    deviation = (most_common_freq - 1 / len(set(text))) ** 2  # Квадратичное отклонение частоты
    return most_common_char, deviation  # Возвращаем символ и его квадратичное отклонение


# === Задача 8 ===
# Задача: рассчитать квадратичное отклонение между ASCII-кодами символов и разницей в ASCII-кодах зеркальных символов.
def quadratic_ascii_deviation(text):
    n = len(text)  # Длина текста
    deviations = []  # Пустой список для хранения отклонений
    for i in range(n // 2):  # Проходим по первой половине строки
        # Разница в ASCII-кодах между зеркальными символами
        difference = abs(ord(text[i]) - ord(text[-(i + 1)]))  # ord() получает код символа
        deviation = (ord(text[i]) - difference) ** 2  # Квадратичное отклонение
        deviations.append((text[i], deviation))  # Добавляем символ и его отклонение в список
    return sorted(deviations, key=lambda x: x[1])  # Сортируем по возрастанию отклонений


# === Задача 9 ===
# Задача: найти квадратичное отклонение дисперсии среднего веса ASCII-кодов троек символов.
def ascii_triple_variance(text):
    n = len(text)  # Длина текста
    variances = []  # Список для хранения квадратичных отклонений дисперсий троек
    for i in range(n - 2):  # Проходим по всем возможным тройкам символов в тексте
        triple = text[i:i + 3]  # Извлекаем тройку символов
        ascii_sum = sum(ord(c) for c in triple)  # Считаем сумму ASCII-кодов тройки
        mean = ascii_sum / 3  # Находим средний вес ASCII-кодов тройки
        # Рассчитываем дисперсию и квадратичное отклонение
        variance = sum((ord(c) - mean) ** 2 for c in triple) / 3  # Средний квадрат отклонений от среднего значения
        variances.append((triple, variance))  # Добавляем тройку и её дисперсию в список
    return sorted(variances, key=lambda x: x[1])  # Сортируем по возрастанию дисперсии


text = "Привет, расскажи что-нибудь интересное"
alphabet_freq = {
    'а': 0.080, 'б': 0.015, 'в': 0.045, 'г': 0.017, 'д': 0.029, 'е': 0.072, 'ё': 0.001,
    'ж': 0.007, 'з': 0.016, 'и': 0.062, 'й': 0.010, 'к': 0.028, 'л': 0.035, 'м': 0.026,
    'н': 0.053, 'о': 0.090, 'п': 0.023, 'р': 0.040, 'с': 0.045, 'т': 0.053, 'у': 0.021,
    'ф': 0.002, 'х': 0.009, 'ц': 0.004, 'ч': 0.012, 'ш': 0.006, 'щ': 0.003, 'ъ': 0.014,
    'ы': 0.016, 'ь': 0.017, 'э': 0.003, 'ю': 0.006, 'я': 0.018
}

freq_diff_result = frequency_difference(text, alphabet_freq)
print("Сортировка символов по увеличению разницы частот:", freq_diff_result)

most_common_char, quad_dev = quadratic_deviation(text)
print(f"Наиболее часто встречаемый символ: '{most_common_char}', квадратичное отклонение: {quad_dev}")

ascii_deviation_result = quadratic_ascii_deviation(text)
print("Квадратичные отклонения между ASCII-кодами пар:", ascii_deviation_result)

triple_variance_result = ascii_triple_variance(text)
print("Квадратичные отклонения дисперсий тройки символов:", triple_variance_result)
