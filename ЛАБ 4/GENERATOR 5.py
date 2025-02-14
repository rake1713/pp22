def countdown(n):
    while n >= 0:
        yield n
        n -= 1
n = int(input("Введите число n: "))
for num in countdown(n):
    print(num, end=" ")