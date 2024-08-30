"""
Assumptions:
1. The score for being a school alumni and volunteer is both 1.
2. Distance score will be calculated by normalizing the euclidean_distance between the student's home location and the school's location.
3. If the score of a student is same among different schools, the student will be allocated to the school with smaller index in the input json.
"""

import json


def euclidean_distance(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def calculate_distances(schools, students):
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

    return distances, min_distance, max_distance


def normalize_distances(distances, min_distance, max_distance, students):
    for (student_id, school_name), distance in distances.items():
        normalized_distance = (distance - min_distance) / (max_distance - min_distance)
        for student in students:
            if student["id"] == student_id:
                student[f"distance_to_{school_name}"] = normalized_distance


def calculate_scores(schools, students):
    all_scores = []

    for school in schools:
        scores = []

        if school["maxAllocation"] == 0:
            continue

        for student in students:
            normalized_distance = student[f"distance_to_{school['name']}"]

            alumni = 1 if school["name"] == student.get("alumni") else 0
            volunteer = 1 if school["name"] == student.get("volunteer") else 0

            score = alumni * 0.3 + volunteer * 0.2 - normalized_distance * 0.5
            scores.append(score)
            all_scores.append((score, student["id"], school["name"]))

    return all_scores


def allocate_students(schools, students, all_scores):
    output_list = []
    filled_student = set()

    all_scores.sort(reverse=True, key=lambda x: x[0])

    for score, student_id, school_name in all_scores:
        school = next(s for s in schools if s["name"] == school_name)

        if school["maxAllocation"] > 0 and student_id not in filled_student:
            found = False
            for key_value in output_list:
                if school["name"] in key_value:
                    key_value[school["name"]].append(student_id)
                    found = True
                    break

            if not found:
                output_list.append({school["name"]: [student_id]})

            filled_student.add(student_id)
            school["maxAllocation"] -= 1

    return output_list


# Main function
def main():

    # Specify the path to your JSON file
    file_path = "input2.json"

    # Open the JSON file and load its contents
    with open(file_path, "r") as file:
        data = json.load(file)

    # Access the data from the JSON file
    schools = data["schools"]
    students = data["students"]

    # Calculate distances and normalize them
    distances, min_distance, max_distance = calculate_distances(schools, students)
    normalize_distances(distances, min_distance, max_distance, students)

    # Calculate scores and allocate students
    all_scores = calculate_scores(schools, students)
    output_list = allocate_students(schools, students, all_scores)

    # # print the output list
    # print(output_list)

    # Write the output list to a JSON file
    output_file_path = "output.json"
    with open(output_file_path, "w") as output_file:
        json.dump(output_list, output_file, indent=4)


# Run the main function
if __name__ == "__main__":
    main()
