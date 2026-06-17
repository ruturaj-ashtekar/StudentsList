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
    searchStudent,
    addStudent,
    delStudent
)

app = Flask(__name__)
app.secret_key = "student_erp_secret"

# Create database/table if not exists
initialize_database()


@app.route("/", methods=["GET"])
def home():
    search = request.args.get("search", "").strip()

    if search:
        students = searchStudent(search)
    else:
        students = listStudents()

    return render_template(
        "index.html",
        students=students,
        search=search
    )


@app.route("/add", methods=["POST"])
def add():
    name = request.form.get("name", "").strip()

    if not name:
        flash("Student name cannot be empty.")
        return redirect(url_for("home"))

    try:
        addStudent(name.capitalize())
        flash(f"{name.capitalize()} added successfully.")
    except Exception as e:
        flash(str(e))

    return redirect(url_for("home"))


@app.route("/delete/<int:student_id>")
def delete(student_id):
    try:
        delStudent(student_id)
        flash("Student removed successfully.")
    except Exception as e:
        flash(str(e))

    return redirect(url_for("home"))


@app.errorhandler(404)
def page_not_found(error):
    return (
        "<h1>404</h1><p>Page not found.</p>",
        404
    )


if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )