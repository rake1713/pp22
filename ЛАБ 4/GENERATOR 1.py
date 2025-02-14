def square_generator(N):
    for i in range(N):
        yield i ** 2
n=int(input())
for square in square_generator(n):
    print(square, end=" ")  