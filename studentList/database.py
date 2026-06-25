import sqlite3

DB_NAME = "students.db"

def connect():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    conn = connect()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
)""")
    
    conn.commit()
    conn.close()

def listStudents():
    conn = connect()
    students = conn.execute("SELECT id, name FROM students ORDER BY name"
    ).fetchall()
    conn.close()
    return students

def searchStudent(name):
        conn = connect()
        result = conn.execute("SELECT * FROM students WHERE name=?",(name,)
        ).fetchone()
        conn.close()
        return result

def searchStudentById(student_id):
        conn = connect()
        result = conn.execute("SELECT * FROM students WHERE id=?",(student_id,)
        ).fetchone()
        conn.close()
        return result

def addStudent(name):
      conn = connect()
      conn.execute(
            "INSERT INTO students(name) VALUES (?)",
            (name,)
      )
      conn.commit()
      conn.close()

def delStudent(name):
    conn = connect()
    conn.execute(
            "DELETE FROM students WHERE name=?",
            (name,)
      )
    conn.commit()
    conn.close()
    
def delStudentById(id):
    conn = connect()
    conn.execute(
            "DELETE FROM students WHERE id=?",
            (id,)
      )
    conn.commit()
    conn.close()
    