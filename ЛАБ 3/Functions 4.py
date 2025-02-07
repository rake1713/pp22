'''Вам дан список чисел, разделенных пробелами. Напишите функцию filter_prime, которая будет 
принимать список чисел в качестве аргумента и возвращать только простые числа из списка.'''


def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def filter_prime(numbers):
    xx=[]
    for x in numbers:
        if is_prime(x):
            xx.append(x)
    return xx

numbers = list(map(int, input("Введите числа через пробел: ").split()))
print(filter_prime(numbers))
