'''Напишите программу для решения классической головоломки: Мы насчитали 35 голов и 94 ноги среди кур и кроликов на ферме. Сколько у 
 нас кроликов и сколько кур? create function: solve(numheads, a):'''
 
 

    # x + y = b  (где x - куры, y - кролики)
    # 2x + 4y = a (у кур 2 ноги, у кроликов 4 ноги)
    
    # Выразим x через y из первого уравнения:
    # x = b - y
    
    # Подставим в второе уравнение:
    # 2(b - y) + 4y = a
    # 2b - 2y + 4y = a
    # 2b + 2y = a
    # 2y = a - 2b
    # y = (a - 2b) / 2
def krolik_kurica(numheads,numlegs):
    y=(numlegs-2*numheads)//2
    x=numheads-y
    print('Krolik',y)
    print('Kurica',x)
    
    
b=int(input())
a=int(input())
krolik_kurica(b,a)