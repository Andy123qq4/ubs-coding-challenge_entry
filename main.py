"""
Assumptions:
1. The score for being a school alumni and volunteer is both 1.
2. The score for being a school volunteer is 1.
3. If the score of a student is same among different schools, the student will be allocated to the school with smaller index in the input json.
"""

import json

# Specify the path to your JSON file
file_path = "input2.json"

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

all_scores = []

for school in schools:
    print("for school", school["name"], ", we have quota", school["maxAllocation"])
    scores = []

    if school["maxAllocation"] == 0:
        print(school["name"], "is full")
        continue

    # for quota in range(school["maxAllocation"]):
    for student in students:
        normalized_distance = student[f"distance_to_{school['name']}"]

        alumni = 0
        volunteer = 0
        if "alumni" in student and student["alumni"] is not None:
            if school["name"] == student["alumni"]:
                alumni = 1
        if "volunteer" in student and student["volunteer"] is not None:
            if school["name"] == student["volunteer"]:
                volunteer = 1
        print(
            "dist=",
            round(normalized_distance, 5),
            "alumni=",
            alumni,
            "volunteer=",
            volunteer,
            end=". ",
        )
        score = alumni * 0.3 + volunteer * 0.2 - normalized_distance * 0.5
        print("student", student["id"], "," + "the score is ", round(score, 5))
        scores.append(score)
        all_scores.append(score)
        # print(scores)
    print(scores)
    # all_scores.append({school["name"]: scores})
    # if there are multiple students with the same maximum score,
    # the code will only return the first occurrence of the maximum score (smaller ID will win)

# sort the scores in descending order
print(all_scores)
print(len(all_scores), len(students))


filled_student = set()
filled_school = set()

for school in schools:
    print(school)

print(len(filled_student), len(students), len(filled_school), len(schools))

# while not (len(filled_student) == len(students) or len(filled_school) == len(schools)):

for i in range(len(all_scores)):
    max_student_score = max(all_scores)
    # print(max_student_score)
    # find the index of the max score
    max_student_score_index = all_scores.index(max_student_score)
    print("max student id index", max_student_score_index)
    # find the student id and school name
    student_id = students[max_student_score_index % len(students)]["id"]
    school = schools[max_student_score_index % len(schools)]
    school_name = school["name"]
    print(school_name, ":", student_id)

    if school["maxAllocation"] > 0 and student_id not in filled_student:
        best = {school_name: [student_id]}
        print(best)

        # append to output list
        found = False
        for key_value in output_list:
            if school["name"] in key_value:
                key_value[school["name"]].append(student_id)
                found = True
                break

        if not found:
            output_list.append(best)

        filled_student.add(student_id)
        print("filled student:", filled_student)
        school["maxAllocation"] -= 1

    # find the next max score
    all_scores[max_student_score_index] = float("-inf")

print(output_list)

"""
for school_score in all_scores:
    school_name = list(school_score.keys())[0]
    print("school_name:", school_name)
    for student_score in school_score:
        if school["name"] == school_name and school["maxAllocation"] > 0:
            best = {school["name"]: [student_id]}
            school["maxAllocation"] -= 1
            schools[schools.index(school)] = school

            found = False
            for key_value in output_list:
                if school["name"] in key_value:
                    key_value[school["name"]].append(student_id)
                    found = True
                    break

            if not found:
                output_list.append(best)

            # Remove the student from the list to avoid reallocation
            students = [student for student in students if student["id"] != student_id]
            break

print(output_list)
"""
