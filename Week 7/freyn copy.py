
classroom_students = {"Sekol":[], "Lucas":[],}
# classroom_students = ["Freyn", "Adelman", "Sekol", "Simms"]

freyn = {
    "name": "Lucas",
    "grade": 92,
    "lab": "Software",
}

adelman = {
    "name": "Marcus",
    "grade": 94,
    "lab": "Cosmetology",
}
sekol = {
    "name": "Michael",
    "grade": 67,
    "lab": "Welding"
}

simms = {
    "name": "Jayden",
    "grade": 91,
    "lab": "Software"
}

students = {
    "Freyn": freyn,
    "Adelman": adelman,
    "Sekol": sekol,
    "Simms": simms,
}

for student_key in classroom_students:
    student = students[student_key]
    print(f"Student name: {student['name']}, Grade: {student['grade']}, Lab: {student['lab']}")

