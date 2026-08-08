import re

url = input("Enter you twitter URL: ").strip()

username = re.sub(r"https://twitter.com",url)

print(f"Your twitter username is {username}")