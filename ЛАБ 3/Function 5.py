#Напишите функцию, которая принимает строку от пользователя и выводит все перестановки этой строки.

from itertools import permutations

def perestanovka(s):
    perms = set(permutations(s))  
    for perm in perms:
        print(''.join(perm))
a = input()
print()
perestanovka(a)
