count = 0

with open("names.txt") as file:
    for line in file:
        if line.startswith("#"):
            continue
        if line.strip() == "":
            continue
        else:
            count += 1

print(f"Number of lines of code: {count}")