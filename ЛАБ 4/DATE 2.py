from datetime import datetime, timedelta
today = datetime.now().date()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)
print("Вчера:", yesterday.strftime("%d-%m-%Y"))
print("Сегодня:", today.strftime("%d-%m-%Y"))
print("Завтра:", tomorrow.strftime("%d-%m-%Y"))