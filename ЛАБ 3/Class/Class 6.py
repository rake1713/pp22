
prostoi = lambda x: x > 1 and all(x % i != 0 for i in range(2, int(x**0.5) + 1))

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

prost = list(filter(prostoi, numbers))

print("Простые числа:", prost)