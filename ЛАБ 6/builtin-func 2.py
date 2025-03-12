def slovo(s):
    up = sum(1 for c in s if c.isupper())
    low = sum(1 for c in s if c.islower())
    return up, low

print(slovo("Hello World!"))  # (2, 8)