"""Server for architecture app."""

import os
from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
from model import connect_to_db, db, Submission, ArchitecturalStructure, User, Like, Album
import crud
from jinja2 import StrictUndefined
import json
import requests
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]
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
    if 'email' in session and 'user_id' in session:
        return redirect(f"/user_dashboard/{session['user_id']}")
    
    return render_template("login.html")


@app.route("/login", methods=['POST'])
def user_login():
    if 'email' in session and 'user_id' in session:
        return redirect(f"/user_dashboard/{session['user_id']}")
    
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)

    if not user or password != user.password:
        flash("Invalid email or password.")
    else:
        session["email"] = user.email
        session["user_id"] = user.user_id
        flash(f"You are now logged in, {user.email}.")
        return redirect(f"/user_dashboard/{user.user_id}")

    return render_template("login.html")


@app.route("/logout", methods=['POST'])
def user_logout():
    session.clear()
    flash("You have been logged out.")
    return redirect("/")


@app.route("/user_dashboard/<user_id>")
def dashboard_page(user_id):
    """View dashboard page."""

    user = crud.get_user_by_id(user_id)
    submissions = db.session.query(Submission).filter_by(user_id=user_id).order_by(Submission.submission_id.desc()).all()
    liked_structures = db.session.query(ArchitecturalStructure.structure_name).join(Like).filter(Like.user_id == user_id, Like.liked == True).all()
    objectives = crud.get_objectives()

    for submission in submissions:
        if submission.status:
            for objective_submission in submission.objectives:
                if objective_submission.objective.objective_description == 'Find a Bauhaus structure':
                    user.obj_bauhaus = True
                elif objective_submission.objective.objective_description == 'Find a Brutalist structure':
                    user.obj_brutalism = True
                elif objective_submission.objective.objective_description == 'Find a Victorian structure':
                    user.obj_victorian = True

    db.session.commit()

    return render_template("dashboard.html", user=user, submissions=submissions, objectives=objectives)


@app.route("/featured")
def featured_page():

    arch_structures = crud.get_arch_structures()
    print(arch_structures)

    return render_template("featured.html", arch_structures=arch_structures)


@app.route("/featured/<structure_id>")
def featured_details_page(structure_id):

    arch_structure = crud.get_arch_structure_by_id(structure_id)
    user_id = session.get('user_id')
    user = crud.get_user_by_id(user_id)

    return render_template("featured-details.html", arch_structure=arch_structure, structure_id=structure_id, user=user)


@app.route("/submitted_structures_map")
def submitted_structures_map():

    return render_template("structure-map.html")


@app.route('/map_data')
def map_data():
    approved_structures = ArchitecturalStructure.query.all()
    print("APPROVED STRUCTURES")
    print(approved_structures)
    locations = []
    
    for arch_structure in approved_structures:
        address = f"{arch_structure.structure_name}, {arch_structure.city}, {arch_structure.country}"
        if arch_structure.state_or_province:
            address += f", {arch_structure.state_or_province}"

        address = address.replace(" ", "%20")
        address = address.replace(",", "")
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key=AIzaSyDSMrST6tA5LevywsZYvPXPsmIqhlbmRg4"
        response = requests.get(url)
        results = response.json()

        if results['status'] == 'OK':
            lat = results['results'][0]['geometry']['location']['lat']
            lng = results['results'][0]['geometry']['location']['lng']

            locations.append({
                'structure_name': arch_structure.structure_name,
                'lat': lat,
                'lng': lng,
            })
        else:
            print(f"Geocoding failed for address: {address}. Status: {results['status']}")

        print(results)
        
    print(f"Locations list: {locations}")

    return jsonify(locations)


@app.route("/db_submit")
def display_submission_form():

    return render_template("db-submission-form.html")


@app.route("/db_submit", methods=['POST'])
def submission():

    user_id = session["user_id"]

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
    
    db_upload_file = request.files["db-upload"]
    db_upload_filename = secure_filename(db_upload_file.filename)
    db_upload_file.save(f"static/img/uploads/{db_upload_filename}")
    db_upload_file_path = f"/static/img/uploads/{db_upload_filename}"

    submission = crud.create_db_submission(user_id, submission_type, user_structure_name, user_structure_type, user_arch_style, user_year_built, user_arch_firm, user_architect_name, user_street_address, user_city, user_state_or_province, user_postal_code, user_country, db_upload_file_path)

    flash("Your have successfully submitted a structure to our database! An admin will either approve or deny your submission within 24 hours.")
    return redirect(f"/user_dashboard/{user_id}")


@app.route("/obj_submit")
def display_submissions_form():

    objectives = crud.get_objectives()

    return render_template("obj-submission-form.html", objectives=objectives)


@app.route("/obj_submit/", methods=['POST'])
def submissions():
    objectives = crud.get_objectives()
    user_id = session["user_id"]
    objective_id = request.form.get("objective-id")

    objective = crud.get_objective_by_id(objective_id)
    submission_type = request.form.get("submission-type")
    objective_description = request.form.get("user-obj")

    obj_upload_file = request.files["obj-upload"]
    obj_upload_filename = secure_filename(obj_upload_file.filename)
    obj_upload_file.save(f"static/img/uploads/{obj_upload_filename}")
    obj_upload_file_path = f"/static/img/uploads/{obj_upload_filename}"

    # submissions = crud.create_obj_submission(user_id, submission_type, objective_description, obj_upload_file_path)

    new_submission = crud.create_obj_submission(user_id, submission_type, objective_description, obj_upload_file_path)

    new_obj_sub = crud.create_obj_sub(objective_id, new_submission.submission_id)

    return redirect(f"/user_dashboard/{user_id}")


@app.route("/admin")
def admin_dashboard():

    submissions = Submission.query.all()

    return render_template("admin-dashboard.html", submissions=submissions)


@app.route('/admin/approve/<submission_id>', methods=['POST'])
def approve_submission(submission_id):
    submission = Submission.query.get(submission_id)

    if submission.submission_type == 'structure':
        submission.status = True
        db.session.commit()

        structure = ArchitecturalStructure(
            user_id=submission.user_id,
            structure_name=submission.user_structure_name,
            structure_type=submission.user_structure_type,
            arch_style=submission.user_arch_style,
            year_built=submission.user_year_built,
            arch_firm=submission.user_arch_firm,
            architect_name=submission.user_architect_name,
            street_address=submission.user_street_address,
            city=submission.user_city,
            state_or_province=submission.user_state_or_province,
            postal_code=submission.user_postal_code,
            country=submission.user_country,
            arch_img_file_path=submission.db_upload_file_path
        )

        db.session.add(structure)
        db.session.commit()

        flash(f"Submission with ID {submission.submission_id} has been approved.")

    if submission.submission_type == 'objective':
        submission.status = True
        db.session.commit()

    return redirect("/admin")


@app.route('/admin/deny/<submission_id>', methods=['POST'])
def deny_submission(submission_id):
    submission = Submission.query.get(submission_id)

    if submission.submission_type == 'structure':
        submission.status = False
        db.session.commit()

    if submission.submission_type == 'objective':
        submission.status = False
        db.session.commit()

    return redirect("/admin")


@app.route('/like_structure/<structure_id>', methods=['POST'])
def like_structure(structure_id):
    user_id = session["user_id"]
    user = User.query.get(user_id)
    structure = ArchitecturalStructure.query.filter_by(structure_id=structure_id).first()

    like = Like.query.filter_by(user_id=user_id, structure_id=structure_id).first()

    if like is None:
        like = Like(user=user, architectural_structure=structure)
        db.session.add(like)
        structure.num_likes += 1
        flash("Added to your likes!")
    else:
        flash("You have already liked this structure!")
    
    db.session.commit()

    flash("Added to your likes!")
    return redirect(f"/user_dashboard/{user.user_id}")


@app.route("/albums/<user_id>")
def albums_page(user_id):
    """Display albums for a specific user."""

    user = crud.get_user_by_id(user_id)
    albums = crud.get_albums_by_user_id(user_id)
    
    return render_template("albums.html", user=user, albums=albums)


@app.route('/create_album/<user_id>')
def show_create_album_form(user_id):
    """Show form to create a new album."""
    
    user = crud.get_user_by_id(user_id)
    
    return render_template('create-album.html', user=user)


@app.route('/create_album/<user_id>', methods=['POST'])
def create_album(user_id):
    """Create a new album."""

    album_name = request.form.get('album-name')
    if album_name:
        album = crud.create_album(user_id=user_id, album_name=album_name)
        user = crud.get_user_by_id(user_id)
        return render_template("create-album.html", user=user, album=album)

    return redirect(f'/create_album/{user_id}')


@app.route('/add_to_album/<structure_id>', methods=['POST'])
def add_to_album(structure_id):
    """Add a structure to an album."""
    
    user_id = session.get("user_id")
    album_id = request.form.get("album-id")
    album_name = request.form.get("album-name")
    
    crud.add_structure_to_album(album_id, structure_id)
    
    flash('Structure added to album!')
    return redirect(f'/albums/{user_id}')


@app.route('/album_details/<album_id>')
def album_details(album_id):
    """Display the details of a specific album."""

    album = crud.get_album_by_id(album_id)
    return render_template('album-details.html', album=album)

    

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)