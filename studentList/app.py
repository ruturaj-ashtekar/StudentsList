from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)
import logging
import sqlite3
from database import (
    initialize_database,
    listStudents,
    searchStudent,
    addStudent,
    delStudent
)

logging.basicConfig(
    filename='programLogs.log',
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s'
)
app = Flask(__name__)
app.secret_key = "student_erp_secret"

# Create database/table if not exists
initialize_database()


@app.route("/")
def home():
    try:
        students = listStudents()
    except Exception as e:
        logging.exception(e)
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
        flash("Name cannot be empty.")
        return redirect(url_for("home"))

    try:
        addStudent(name.capitalize())

        logging.info(
            f"Student {name.capitalize()} added."
        )

        flash(
            f"{name.capitalize()} has been added."
        )

    except sqlite3.IntegrityError:

        logging.warning(
            f"Duplicate student attempted: {name}"
        )

        flash(
            f"{name.capitalize()} already exists."
        )

    except sqlite3.DatabaseError as e:

        logging.exception(e)

        flash(
            f"Database error: {e}"
        )

    except Exception as e:

        logging.exception(e)

        flash(
            f"Unexpected error: {e}"
        )

    return redirect(url_for("home"))


@app.route("/search")
def search():

    query = request.args.get(
        "search",
        ""
    ).strip()

    if not query:

        flash(
            "Name cannot be empty."
        )

        return redirect(
            url_for("home")
        )

    try:

        result = searchStudent(
            query.capitalize()
        )

        logging.info(
            f"Student searched: {query}"
        )

        return render_template(
            "index.html",
            students=result,
            search=query
        )

    except sqlite3.DatabaseError as e:

        logging.exception(e)

        flash(
            f"Database error: {e}"
        )

    except Exception as e:

        logging.exception(e)

        flash(
            f"Unexpected error: {e}"
        )

    return redirect(
        url_for("home")
    )


@app.route(
    "/delete/<student_name>"
)
def delete(student_name):

    try:

        deleted = delStudent(
            student_name.capitalize()
        )

        if deleted:

            logging.info(
                f"Student removed: {student_name}"
            )

            flash(
                f"{student_name.capitalize()} removed."
            )

        else:

            flash(
                f"{student_name.capitalize()} not found."
            )

    except sqlite3.DatabaseError as e:

        logging.exception(e)

        flash(
            f"Database error: {e}"
        )

    except Exception as e:

        logging.exception(e)

        flash(
            f"Unexpected error: {e}"
        )

    return redirect(
        url_for("home")
    )


if __name__ == "__main__":
    app.run(
        debug=False,
        host="0.0.0.0",
        port=5000
    )