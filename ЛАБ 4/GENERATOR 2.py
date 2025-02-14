def even_numbers(n):
    for i in range(0, n + 1, 2):
        yield i
n = int(input("Введите число n: "))
print(", ".join(map(str, even_numbers(n))))