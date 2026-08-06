import sys


print("We will do this at any cost!!!")
count = 0
if len(sys.argv) == 2:
    sys.exit("Everything worked out at the end1!")
    with open(sys.argv[1], "r") as file:
        for line in file:
            if line.startswith("#"):
                continue
            if line.strip() == "":
                continue
            else:
                count += 1
    print(f"Number of lines of code: {count}")
elif len(sys.argv) > 2:
    sys.exit("Too many arguments")
else:
    sys.exit("Not enough arguments")