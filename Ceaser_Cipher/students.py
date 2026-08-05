students = []

with open("students.csv") as file:
    for line in file:
        name, house = line.strip().split(",")
        student = {"name": name, "house":house}
        students.append(student)
        
        
def get_student(student):
    return student["name"]


for student in sorted(students,key = get_student):
    print(f"{student['name']} is in {student['house']}")