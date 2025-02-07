"""Определите класс с именем Rectangle, который наследует от Shapeкласса из задачи 2. Экземпляр
класса может быть создан с помощью lengthи width. RectangleКласс имеет метод, который может вычислить area."""


from Class2 import Shape

class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length 
        self.width = width  
    def area(self):
        return self.length * self.width
rectangle = Rectangle(4, 6)
print("Area of Rectangle:", rectangle.area())