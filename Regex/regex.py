import re

ip = input("Enter your ip address: ").strip()
if matches := re.search(r"^(\d+)\.(\d+).(\d+)\.(\d+)$",ip):
    ip_1,ip_2,ip_3,ip_4 =ip.split(".") 
    ip_1 = int(ip_1)
    ip_2 = int(ip_2)
    ip_3 = int(ip_3)
    ip_4 = int(ip_4)
    for part in matches.groups():
        if int(part) < 255:
            print("hh")