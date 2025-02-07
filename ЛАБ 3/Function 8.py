#Напишите функцию, которая принимает список целых чисел и возвращает True, если он содержит их 007в определенном порядке.


def agent007(n):
    for i in range(len(n)-1):
        if n[i-1]==0 and n[i]==0 and n[i+1]==7:
            return True
    return False
a=list(map(int,input().split()))
print(agent007(a))