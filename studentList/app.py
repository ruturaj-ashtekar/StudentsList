from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)
import logging
from database import (
    initialize_database,
    listStudents,
    addStudent,
    searchStudent,
    delStudent
)

app = Flask(__name__)
app.secret_key = "student_secret"

initialize_database()


@app.route("/")
def home():

    try:
        students = listStudents()

    except Exception as e:
        flash(f"Error loading students: {e}")
        students = []

    return render_template(
        "index.html",
        students=students
    )

@app.route("/operation", methods=["POST"])
def operation():

    try:
        operation = request.form.get("operation")
        name = request.form.get("name", "").strip()

        if operation == "list":
            students = listStudents()
            return render_template (
                "index.html",
                students=students
            )
        
        elif operation == "search":

            if not name:
                flash("Name cannot be empty.")
                return redirect("/")
            student = searchStudent(name)

            if student:
                flash(f"{name.capitalize()} fount.")
            else:
                flash(f"{name.capitalize()} not found.")
        elif operation == "add":
            if not name:
                flash("Name cannot be empty.")
                return redirect("/")
            addStudent(name)
            flash(f"{name.capitalize()} added successfully.")
        elif operation == "delete":
            if not name:
                flash("Name cannot be empty.")
                return redirect("/")
            removed = delStudent(name)

            if removed:
                flash(f"{name.capitalize()} removed successfully")
            else:
                flash(f"{name.capitalize()} not found.")
    except Exception as e:
        logging.exception(e)
        flash(str(e))

    return redirect("/")      





@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=True)