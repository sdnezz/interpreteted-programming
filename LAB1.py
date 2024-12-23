#######1st lab####
# polualex@mail.ru
#variant 9 Duka V. 39/2
import math

#Метод нахождения масимального простого делителя
def MaxProstDel(num):
    i = 1
    maxdel = 1
    while i*2<=num:
        if num % i == 0:
            count = 0
            for j in range (1,i+1):
                if i%j == 0:
                    count+=1
            if count == 2 and i> maxdel:
                maxdel=i
                i+=1
            else: i+=1
        else: i+=1
    return maxdel

#Метод нахождения произведения цифр числа, не делящихся на 5
def ProizvCifrNeDelNa5(num):
    num
    proiz = 1
    c=0
    while(num):
        c = num % 10
        if(c % 5 != 0):
            proiz *= c
        num = num//10
    return proiz

#Метод нахождения НОД максимального нечетного делителя числа и произведения цифр данного числа
def NOD_MaxNechetNeprostDel_AND_ProizvCifr(num):
    ProizvCifr = 1
    #Максимальный нечетный непростой делитель
    i = 1
    MaxNechetNeprostDel = 1
    while i * 2 <= num:
        if num % i == 0:
            count = 0
            for j in range(1, i + 1):
                if i % j == 0:
                    count += 1
            if count > 2 and i % 2 != 0 and i > MaxNechetNeprostDel:
                MaxNechetNeprostDel = i
                i += 1
            else:
                i += 1
        else:
            i += 1
    #Произведение цифр числа
    while (num >= 1):
        c = 1
        c = num % 10
        ProizvCifr *= c
        num = num//10
    print("Произведение цифр:",ProizvCifr, "Максимальный непростой нечетный делитель:", MaxNechetNeprostDel)
    #НОД
    while MaxNechetNeprostDel!=ProizvCifr:
        if MaxNechetNeprostDel > ProizvCifr:
            MaxNechetNeprostDel = MaxNechetNeprostDel - ProizvCifr
        else:
            ProizvCifr = ProizvCifr - MaxNechetNeprostDel
    return ProizvCifr

#Ввод числа пользователем

num = int(input("Введите число:"))
print("1) Нахождение масимального простого делителя:", MaxProstDel(num))
print("2) Произведение цифр числа, не делящихся на 5:", ProizvCifrNeDelNa5(num))
print("3) НОД максимального нечетного непростого делителя числа и произведения цифр данного числа:", NOD_MaxNechetNeprostDel_AND_ProizvCifr(num))