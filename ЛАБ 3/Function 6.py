# Напишите функцию, которая принимает строку от пользователя и возвращает
# предложение с переставленными словами. We are ready -> ready are We


def stroka(n):
    return ' '.join(n.split()[::-1])
a = input()
print(stroka(a))