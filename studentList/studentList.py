import sqlite3


conn = sqlite3.connect('students.db')
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
)
""")
conn.commit()



def studentList():
    def listStudents():
        
        print('\nStudent list:')
        cursor.execute("SELECT name FROM students ORDER BY name")
        students = cursor.fetchall()

        if not students:
            print("\nNo students in the list/database.\n")
            return
        print("\n Students List:")
        for index, (name,)in  enumerate(students, start = 1):
            print(f"{index}. {name}")
        print('-' * 8)

    def searchStudents():
        search = input('Enter the name of the student to search: ').strip()
        if not search:
            print('\nName cannot be empty.\n')
            return

        name = search.capitalize()
        
        cursor.execute(
            "SELECT 1 FROM students WHERE name = ?", (name,)
        )
        if cursor.fetchone():
            print(f'\n{name} is in the list and DB.\n')
        else:
            print(f'\n{name} is not in the DB')


    def addStudents():
        nameAdd = input('Enter the name of the student: ').strip()
        if not nameAdd:
            print('\nName cannot be empty.\n')
            return

        name = nameAdd.capitalize()
        try: 
            cursor.execute("INSERT INTO students (name) VALUES (?)", (name,))
            conn.commit()
            print(f'\n{name} has been added to the list and DB.\n')
        except sqlite3.IntegrityError:
            print(f'\n{name} is already in the list.\n')

    def removeStudents():
        toRemove = input('Enter the name of the student to remove: ').strip()
        if not toRemove:
            print('\nName cannot be empty.\n')
            return

        name = toRemove.capitalize()
        cursor.execute("DELETE FROM students WHERE name = ?", (name,))
        if cursor.rowcount > 0:
            conn.commit()
            print(f'\n{name} has been removed from the list.\n')
        else:
            print(f'\n{name} is not in the list.\n')
        

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
                conn.close()
                print('Exiting the program.')
                break
            else:
                print('Invalid option. Please try again.')
    except KeyboardInterrupt:
        print('\nexited!')


if __name__ == '__main__':
    studentList()
