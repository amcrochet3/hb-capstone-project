"""Server for architecture app."""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def homepage():

    return render_template("index.html")


@app.route("/register")
def registration_page():

    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register_user():

    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)

    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        new_user = crud.create_user(fname, lname, email, password)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/login")


@app.route("/login")
def login_page():

    return render_template("login.html")


@app.route("/login", methods=['POST'])
def user_login():

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)

    if not user or password != user.password:
        flash("Invalid email or password.")
    else:
        session["email"] = user.email
        flash(f"You are now logged in, {user.email}.")

    return redirect("/dashboard")


@app.route("/dashboard")
def dashboard_page():
    """View dashboard page."""

    return render_template("dashboard.html")


@app.route("/featured")
def featured_page():

    arch_structures = crud.get_arch_structures()

    return render_template("featured.html", arch_structures=arch_structures)


@app.route("/featured/<structure_id>")
def featured_details_page(structure_id):

    arch_structure = crud.get_arch_structure_by_id(structure_id)

    return render_template("featured_details.html", arch_structure=arch_structure, structure_id=structure_id)


@app.route("/submission_type")
def choose_submission_type():

    return render_template("submission-type.html")


@app.route("/submission_type", methods=['POST'])
def redirect_submission_type():

    submission_type = request.form.get("submission-type")

    if submission_type == "db-submission-type":
        return redirect("/db_submit")
    else:
        return redirect("/")


@app.route("/db_submit")
def submission_form():

    return render_template("db-submission-form.html")


@app.route("/db_submit", methods=['POST'])
def user_submission():

    submission_type = request.form.get("submission-type")
    user_structure_name = request.form.get("user-structure-name")
    user_structure_type = request.form.get("user-structure-type")
    user_arch_style = request.form.get("user-arch-style")
    user_year_built = request.form.get("user-year-built")
    user_arch_firm = request.form.get("user-arch-firm")
    user_architect_name = request.form.get("user-architect-name")
    user_street_address = request.form.get("user-street-address")
    user_city = request.form.get("user-city")
    user_state_or_province = request.form.get("user-state-or-province")
    user_postal_code = request.form.get("user-postal-code")
    user_country = request.form.get("user-country")
    user_img_url = request.form.get("user-img-url")
    submission_complete = True

    submission = crud.create_submission(submission_type, user_structure_name, user_structure_type, user_arch_style, user_year_built, user_arch_firm, user_architect_name, user_street_address, user_city, user_state_or_province, user_postal_code, user_country, user_img_url, submission_complete)

    if submission:
        flash("Submission received.")

    return render_template("submit.html",
                            submission_type=submission_type,
                            user_structure_name=user_structure_name,
                            user_structure_type=user_structure_type,
                            user_arch_style=user_arch_style,
                            user_year_built=user_year_built,
                            user_arch_firm=user_arch_firm,
                            user_architect_name=user_architect_name,
                            user_street_address=user_street_address,
                            user_city=user_city,
                            user_state_or_province=user_state_or_province,
                            user_postal_code=user_postal_code,
                            user_country=user_country,
                            user_img_url=user_img_url,
                            submission_complete=submission_complete)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)