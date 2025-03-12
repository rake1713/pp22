import os

def файлы(path):
    print("Directories:", [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))])
    print("Files:", [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
    print("All contents:", os.listdir(path))

path = "ЛАБ 1"  
файлы(path)