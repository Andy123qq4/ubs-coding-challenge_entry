"""
Assumptions:
1. The score for being a school alumni is 1.
2. The score for being a school volunteer is 1.
"""

import json

# Specify the path to your JSON file
file_path = "input.json"

# Open the JSON file and load its contents
with open(file_path, "r") as file:
    data = json.load(file)

# Access the data from the JSON file
# For example, if your JSON file contains a list of names:
schools = data["schools"]
students = data["students"]
output_list = []


def euclidean_distance(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


distances = {}
min_distance = float("inf")
max_distance = float("-inf")

for school in schools:
    for student in students:
        distance = euclidean_distance(
            school["location"][0],
            school["location"][1],
            student["homeLocation"][0],
            student["homeLocation"][1],
        )
        distances[(student["id"], school["name"])] = distance
        if distance < min_distance:
            min_distance = distance
        if distance > max_distance:
            max_distance = distance

# Normalize distances and store them in the input data
for (student_id, school_name), distance in distances.items():
    normalized_distance = (distance - min_distance) / (max_distance - min_distance)
    for student in students:
        if student["id"] == student_id:
            student[f"distance_to_{school_name}"] = normalized_distance


for school in schools:
    scores = []

    if school["maxAllocation"] == 0:
        continue

    for student in students:
        # distance = euclidean_distance(
        #     school["location"][0],
        #     school["location"][1],
        #     student["homeLocation"][0],
        #     student["homeLocation"][1],
        # )

        normalized_distance = student[f"distance_to_{school['name']}"]

        alumni = 0
        volunteer = 0
        if "alumni" in student and student["alumni"] is not None:
            if school["name"] == student["alumni"]:
                alumni = 1
        if "volunteer" in student and student["volunteer"] is not None:
            if school["name"] == student["volunteer"]:
                volunteer = 1
        print("dist=", normalized_distance, "alumni=", alumni, "volunteer=", volunteer)
        score = alumni * 0.3 + volunteer * 0.2 - normalized_distance * 0.5
        print(school["name"], ",", student["id"], "," + "the score is ", score)
        scores.append(score)

    best_student = students[scores.index(max(scores))]
    output = {school["name"]: [best_student["id"]]}
    print(output)
    school["maxAllocation"] -= 1
    schools[schools.index(school)] = school
    students.remove(best_student)
    if output_list:
        for i in output_list:
            if school["name"] in i:
                i[school["name"]].append(best_student["id"])
                break
        else:
            output_list.append(output)
    # output_list.append(output)
    print()

print(output_list)
# print()
# students = data["students"]
# print(students)
