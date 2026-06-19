from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

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


@app.route("/add", methods=["POST"])
def add():

    name = request.form.get("name", "").strip()

    if not name:
        flash("Name cannot be empty")
        return redirect(url_for("home"))

    try:
        addStudent(name.capitalize())
        flash("Student added successfully")

    except Exception as e:
        flash(str(e))

    return redirect(url_for("home"))


@app.route("/search")
def search():

    name = request.args.get("name", "").strip()

    if not name:
        flash("Name cannot be empty")
        return redirect(url_for("home"))

    student = searchStudent(name.capitalize())

    return render_template(
        "search_result.html",
        student=student,
        search_term=name
    )


@app.route("/delete/<int:student_id>")
def delete(student_id):

    try:
        delStudent(student_id)
        flash("Student deleted successfully")

    except Exception as e:
        flash(str(e))

    return redirect(url_for("home"))


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=True)