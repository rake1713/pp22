import time
import math

def nn(n, a):
    time.sleep(a / 1000)
    print(f"Square root of {n} after {a} ms is {math.sqrt(n)}")

nn(25100, 2123)