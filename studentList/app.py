from flask import Flask, jsonify, request
import logging

from database import (
    initialize_database,
    listStudents,
    addStudent,
    searchStudent,
    searchStudentById,
    delStudent,
    delStudentById
)

app = Flask(__name__)
app.secret_key = "student_secret"

initialize_database()


@app.route('/')
def StudentPortal():
    return "Student Listing Portal"

@app.route('/listStudents')
def listAll():
    students = listStudents()
    return jsonify({
        "students": [
            {
                "id": student["id"],
                "name": student["name"]
            }
            for student in students
        ]
    })

@app.route('/addStd', methods=["POST"])
def add_students():
    try:
        data = request.get_json()
        name = data.get('name')

        if not name:
            return jsonify({
                'success':False,
                'message': "Name is required"
            }),400
        addStudent(name)

        return jsonify({
            "success":True,
            "message":f"{name} added successfully"
        }), 201
    except Exception as e:
        return jsonify({
            "success":False,
            "error":str(e)
        }),500

@app.route('/searchStd/', methods=["GET"])
def searchStd():
    student_name = request.args.get('name')
    student_id = request.args.get('id')
    
    if student_id:
        student = searchStudentById(student_id)
    elif student_name :
        student = searchStudent(student_name)
    else:
        return jsonify({
            "error":"provide id or name"
        }),400
    if not student:
        return jsonify({
            "error":"Student not found"
        }),404
    return jsonify({
        "id": student["id"],
        "name":student["name"]
    })

@app.route('/deleteStd/', methods=['DELETE'])
def delStd():
    student_name = request.args.get('name')
    student_id = request.args.get('id')
    if student_id:
        deleted = delStudentById(student_id)
    elif student_name:
        deleted = delStudent(student_name)
    
    else:
        return jsonify({
            'error': "name or id is required"
        }),400
    if not deleted:
        return jsonify({
            'message': "Student not found"
        }),404
    return jsonify({
        "message":"Student deleted successfully"
    }),200
    
if __name__ == "__main__":
    app.run(debug=True)