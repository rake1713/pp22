from datetime import datetime
a = datetime.now().replace(microsecond=0)
print("Дата и время без микросекунд:", a)