def aaa(filename, lst):
    with open(filename, "w", encoding="utf-8") as file:
        for item in lst:
            file.write(str(item) + "\n")

aaa("ЛАБ 6/row.txt", ["apple", "banana", "cherry"])