"""
                Определите функцию histogram(), 
                которая берет список целых чисел и выводит гистограмму на экран. 
                Например, histogram([4, 9, 7])должна вывести следующее:

"""
def histogram(n):
    for i in n:
        print(i * '*')
a=list(map(int,input().split()))
histogram(a)