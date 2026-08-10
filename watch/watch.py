import re

um = input("Enter your text: ").strip()


print(len(re.findall(r"um", um)))
