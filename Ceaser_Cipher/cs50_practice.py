names = []

with open("names.txt") as file:
    for name in file:
        names.append(name.strip())
for name in sorted(names):
    print("Hello,", name)
        