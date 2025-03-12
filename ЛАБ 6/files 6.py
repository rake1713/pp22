import os
import string
folder = "ЛАБ 6"
for letter in string.ascii_uppercase:
    file_path = os.path.join(folder, f"{letter}.txt")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(f"This is {letter}.txt")

print(f"Файлы A-Z созданы в папке '{folder}'!")