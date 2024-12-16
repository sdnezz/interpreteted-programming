#Вариант: ((8 - 1) %13 ) +1 ) , где 8 – номер по списку.
#Дука В. 39.2 лаб. 6
# Читаем количество английских слов
N = int(input("Введите количество слов: "))

# Словарь для хранения латинско-английских соответствий
latin_to_english = {}

# Читаем английские слова и их переводы
for _ in range(N):
    line = input().strip()
    english_word, latin_words = line.split(' - ')
    latin_words_list = latin_words.split(', ')

    # Обрабатываем каждый латинский перевод
    for latin_word in latin_words_list:
        if latin_word not in latin_to_english:
            latin_to_english[latin_word] = []
        latin_to_english[latin_word].append(english_word)

# Сортируем латинские слова лексикографически
sorted_latin_words = sorted(latin_to_english.keys())

# Выводим результаты
print(len(sorted_latin_words))  # Выводим количество уникальных латинских слов
for latin_word in sorted_latin_words:
    # Для каждого латинского слова сортируем соответствующие английские слова
    english_words_sorted = sorted(latin_to_english[latin_word])
    # Выводим латинское слово и его переводы на английский
    print(f"{latin_word} - {', '.join(english_words_sorted)}")
