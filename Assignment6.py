# Dictionary to store student information
student = {
    "name": "Bent Ten",
    "age": 17,
    "grades": [90, 93, 96]  # list of grades
}
def display_student_info(student_dict):
    """Display the student's information."""
    print("\n--- Student Information ---")
    print(f"Name: {student_dict['name']}")
    print(f"Age: {student_dict['age']}")
    print(f"Grades: {student_dict['grades']}")
    avg = sum(student_dict['grades']) / len(student_dict['grades'])
    print(f"Average Grade: {avg:.2f}")

def update_student_grade(student_dict, new_grade):
    """Add a new grade to the student's grade list."""
    student_dict["grades"].append(new_grade)
    print(f"\nGrade {new_grade} added successfully.")

def update_student_age(student_dict, new_age):
    """Update the student's age."""
    student_dict["age"] = new_age
    print(f"\nAge updated to {new_age}.")
#Calling Function
display_student_info(student)
update_student_grade(student, 85)  # add a new grade
update_student_age(student, 17)    # update age
display_student_info(student)      # show updated info
