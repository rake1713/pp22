'''Определите класс с именем Shapeи его подкласс Square. SquareКласс имеет initфункцию, которая принимает lengthв 
качестве аргумента . Оба класса имеют areaфункцию, которая может вывести площадь фигуры, где площадь фигуры по умолчанию равна 0.'''
class Shape:
    def __init__(self):
        self.area_value = 0 

    def area(self):
        return self.area_value

class Square(Shape):
    def __init__(self, length):
        super().__init__()
        self.length = length 

    def area(self):
        return self.length ** 2
shape = Shape() 
print("Area of Shape:", shape.area()) 
square = Square(5)
print("Area of Square:", square.area()) 