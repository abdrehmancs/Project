import re

link = input("Enter your link: ").strip()

pattern = r"src=(.*?)"

if matches := re.search(pattern, link):
    print("Valid YouTube embed link")