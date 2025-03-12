def bbb(tpl):
    return all(tpl)

print(bbb((True, True, True)))  # True
print(bbb((True, False, True)))  # False