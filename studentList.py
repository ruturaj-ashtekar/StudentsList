
def studentList():
    def listStudents():
        for item in students:
            index = students.index(item)
            sr_no = index + 1
            print(f"{sr_no}. {item}")
    students = []
    try:
        while True:
            if students == []:
                nameAdd = input("Enter the name of the student: ")
                students.append(nameAdd.capitalize())
                listStudents()
            elif students != []:
                nameAdd = input("Enter the name of the student: ")
                students.append(nameAdd.capitalize())
                listStudents()
                remove = input("Do you want to remove any student? (y/n): ")
                if remove.lower() == "y":
                    toRemove = input("Enter the name of the student to remove: ")
                    students.remove(toRemove.capitalize())
                    listStudents()
    except KeyboardInterrupt:
        print("exited!")

if __name__ == "__main__":
    studentList()
