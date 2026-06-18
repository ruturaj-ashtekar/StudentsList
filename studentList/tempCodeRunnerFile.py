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