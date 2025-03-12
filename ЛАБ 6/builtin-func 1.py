def kobeitu(lst):
    res = 1
    for n in lst:
        res *= n
    return res

print(kobeitu([2, 3, 4, 5]))  