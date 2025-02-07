"""Напишите функцию Python, которая принимает список и возвращает новый 
список с уникальными элементами первого списка. Примечание: не используйте collection set."""

def tiposet(n):
    pustoi=[]
    for i in n:
        if i not in pustoi:
            pustoi.append(i)
    return pustoi
a=list(map(int,input().split()))
print(tiposet(a))