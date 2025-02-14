from datetime import datetime
a = datetime(2024, 2, 1, 12, 0, 0)
b = datetime(2024, 2, 10, 15, 30, 0)
c = (b - a).total_seconds()
print("Разница в секундах:", c)