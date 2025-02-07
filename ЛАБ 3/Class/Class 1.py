'''Определите класс, который имеет как минимум два 
метода: getString: для получения строки из консольного ввода printString: для вывода строки в верхнем регистре.'''

class strr:
    def __init__(self):
        self.text = ""
    def getString(self):
        self.text = input("Enter a string = ")
    def printString(self):
        print(self.text.upper())
стр = strr()
стр.getString()
стр.printString()