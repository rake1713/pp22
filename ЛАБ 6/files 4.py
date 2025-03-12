def counts(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return sum(1 for line in file)

filename = "README.md"  
print("Number of lines:", counts(filename))