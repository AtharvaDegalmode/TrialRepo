Student_Info={"name":"BenTen",
         "age":17,
         "grades":[93,90,96]}

def display_studentinfo(dict_student):
    avg_grades=sum(dict_student["grades"])/len(dict_student["grades"])    
    print(dict_student,avg_grades)
def update_student_grade(dict_student,grades):
    dict_student["grades"].append(grades)
    print("Updated info:",dict_student)
    print("Updated Average:",sum(dict_student["grades"])/len(dict_student["grades"]))
def update_student_age(dict_student,new_age):
    dict_student["age"].append(new_age)  
    print("Updated Info:",dict_student)  
def update_student_name(dict_student,new_name):
    dict_student["name"].append(new_name)
    print("updated_Info:",Student_Info)
display_studentinfo(Student_Info)



   
  





   
  
   


