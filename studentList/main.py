import sqlite3
import logging
from flask import Flask





logging.basicConfig(
    filename='programLogs.log',
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s'
)



try:
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
except sqlite3.Error as e:
    print("failed to connect \nOccuring Error: {e}")


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
        
        try:    
            cursor.execute("SELECT name FROM students ORDER BY name")
            students = cursor.fetchall()
        except sqlite3.DatabaseError as e:
            print(f"database error: {e}")

        except Exception as e:
            print(f"unexpected error: {e}")
        
        if not students:
            print("\nNo students in the list/database.\n")
            return
        for index, (name,)in  enumerate(students, start = 1):
            print(f"{index}. {name}")

    def searchStudents():
        try: 
            while True:
                search = input('\nEnter the name of the student to search: ').strip()
                if not search:
                    print('\nName cannot be empty.\n')
                    return
                elif search == "exit":
                    return
                elif search == "list":
                    listStudents()

                name = search.capitalize()
                

                cursor.execute(
                    "SELECT 1 FROM students WHERE name = ?", (name,)
                )
                
                result = cursor.fetchone()
                if result:
                    print(f'\n{name} is in the list and DB. (Position : {result[0]}).\n')
                    logging.info(f"name:{name} was searched")
                else:
                    print(f'\n{name} is not in the DB')
        except KeyboardInterrupt:
            studentList()

    def addStudents():
        try: 
            while True:
                nameAdd = input('\nEnter the name of the student: ').strip()
                if not nameAdd:
                    print('\nName cannot be empty.\n')
                    return
                elif nameAdd == "exit":
                    return
                elif nameAdd == "list":
                    listStudents()
                    continue
                name = nameAdd.capitalize()
                try: 
                    cursor.execute("INSERT INTO students (name) VALUES (?)", (name,))
                    conn.commit()
                    print(f'\n{name} has been added to the list and DB.\n')
                    logging.info("name: {name} is added to the List/DB")
                except sqlite3.IntegrityError:
                    print(f'\n{name} is already in the list.\n')
                    logging.warning(f"Duplicate student attempted: {name}")
                except sqlite3.DatabaseError as e:
                    print(f"database error: {e}")
                    logging.exception(f"error occured : {e}")
                except Exception as e:
                    print(f"enexpected error: {e}")
                    logging.exception(f"Unexpected error occured {e}")        
        except KeyboardInterrupt:
            studentList()

    def removeStudents():
        try:
            while True:
                toRemove = input('\nEnter the name of the student to remove: ').strip()
                if not toRemove:
                    print('\nName cannot be empty.\n')
                    return
                elif toRemove == "exit":
                    return
                elif toRemove == "list":
                    listStudents()
                    continue

                name = toRemove.capitalize()
                try: 
                    cursor.execute("DELETE FROM students WHERE name = ?", (name,))
                except sqlite3.DatabaseError as e :
                    print(f"Database error: {e}")
                    logging.exception(f"error occured: {e}")
                except Exception as e :
                    print(f"unexpected error: {e}")
                    logging.exception(f"unexpected error occured: {e} ")
                if cursor.rowcount > 0:
                    conn.commit()
                    print(f'\n{name} has been removed from the list.\n')
                    logging.info(f"Student: {name} removed from list")
                else:
                    print(f'\n{name} is not in the list.\n')
        except KeyboardInterrupt :
            studentList()
        
    try:
        while True:
            menu = ('\n'
                '1. List Students\n'
                '2. Search Students\n'
                '3. Add Students\n'
                '4. Remove Students\n'
                '5. Exit'
                '\n'
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
            elif userInput == '5' or userInput == 'exit':
                conn.close()
                print('Exiting the program.')
                break
            else:
                print('Invalid option. Please try again.')
    except KeyboardInterrupt:
        print('\nexited!')


if __name__ == '__main__':
    studentList()
