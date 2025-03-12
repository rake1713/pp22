def copy_file(source, destination):
    with open(source, "r", encoding="utf-8") as src, open(destination, "w", encoding="utf-8") as dest:
        dest.write(src.read())

copy_file("ЛАБ 5/row.txt", "ЛАБ 6/destination.txt")