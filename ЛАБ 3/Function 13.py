"""Напишите программу, способную играть в "Guess the number"игру, в которой угадываемое число 
выбирается случайным образом в диапазоне от 1 до 20. Вот как это должно работать при запуске в терминале:"""

import random
print("Hello! What is your name?")
name = input()
print("Well,", name," I am thinking of a number between 1 and 20.")
x = random.randint(1, 20)
popitka = 0
while True:
    print("Take a guess.")
    a = int(input())
    popitka += 1
    if a == x:
        print("Good job," ,name,"! You guessed my number in ",popitka," guesses!")
        break
    elif a < x:
        print("Your guess is too low.")
    else:
        print("Your guess is too high.")