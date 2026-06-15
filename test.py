def studentList():
    def listStudents():
        if not students:
            print('\n"No students in the list."\n')
            return

        print('\nStudent list:')
        for index, student in enumerate(students, start=1):
            print(f'{index}. {student}')
        print('-' * 8)

    def searchStudents():
        search = input('Enter the name of the student to search: ').strip()
        if not search:
            print('\nName cannot be empty.\n')
            return

        name = search.capitalize()
        if name in students:
            print(f'\n{name} is in the list.\n')
        else:
            print(f'\n{name} is not in the list.\n')

    def addStudents():
        nameAdd = input('Enter the name of the student: ').strip()
        if not nameAdd:
            print('\nName cannot be empty.\n')
            return

        students.append(nameAdd.capitalize())
        print(f'\n{nameAdd.capitalize()} has been added to the list.\n')

    def removeStudents():
        toRemove = input('Enter the name of the student to remove: ').strip()
        if not toRemove:
            print('\nName cannot be empty.\n')
            return

        name = toRemove.capitalize()
        if name in students:
            students.remove(name)
            print(f'\n{name} has been removed from the list.\n')
        else:
            print(f'\n{name} is not in the list.\n')

    students = []
    try:
        while True:
            menu = (
                '1. List Students\n'
                '2. Search Students\n'
                '3. Add Students\n'
                '4. Remove Students\n'
                '5. Exit'
            )
            print(menu)
            userInput = input('Choose an option: ').strip()

            if userInput == '1':
                listStudents()
            elif userInput == '2':
                searchStudents()
            elif userInput == '3':
                addStudents()
            elif userInput == '4':
                removeStudents()
            elif userInput == '5':
                print('Exiting the program.')
                break
            else:
                print('Invalid option. Please try again.')
    except KeyboardInterrupt:
        print('\nexited!')


if __name__ == '__main__':
    studentList()
