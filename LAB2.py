#######2nd Lab####
# variant 9 Duka V. 39/2
import random
import math
# Перемешивание слов в строке
def shufflewords(str):
    words = str.split()
    for i in range(len(words)):
        j = random.randint(0, i)
        words[i], words[j], = words[j], words[i]
    str_shuffle = ' '.join(words)
    return str_shuffle

# Подсчет слов с четным количеством символов
def countletters(str):
    words = str.split()
    count = sum(1 for word in words if len(word) % 2 == 0)
    return count

# БСК флаг России - упорядоченный массив строк
def white_blue_red(colors):
    order = ["белый", "синий", "красный"]
    colors.sort(key=lambda color: order.index(color))
    return colors


print("Введите строку слов через пробел:")
str = str(input())
print("3) Перемешанная строка слов: ", shufflewords(str))
print("8) Количество слов в строке с четным количеством символов:", countletters(str))
colors = ["синий", "красный", "белый"]
print("16) Упорядоченный массив строк:", white_blue_red(colors))
