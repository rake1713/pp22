from datetime import datetime, timedelta
a = datetime.now()
b = a - timedelta(days=5)
print("Дата 5 дней назад:", b.strftime("%d-%m-%Y"))