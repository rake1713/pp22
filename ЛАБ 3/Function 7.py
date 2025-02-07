#Для заданного списка целых чисел вернуть True, если массив содержит 3 рядом с 3 где-либо.
"""
def has_33(nums):
    pass

has_33([1, 3, 3]) → True
has_33([1, 3, 1, 3]) → False
has_33([3, 1, 3]) → False

"""

def pp2(n):
    for i in range(len(n)-1):
        if n[i]==3 and n[i+1]==3:
            return True
    return False
a=list(map(int,input().split()))
print(pp2(a))