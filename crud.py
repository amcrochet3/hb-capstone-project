"""CRUD Operations"""

from model import db, ArchitecturalStructure, User, Like, Album, Objective, Submission, connect_to_db

def create_user(fname, lname, email, password):
    """Create and return a new user."""

    user = User(fname=fname, lname=lname, email=email, password=password)

    return user


def create_arch_strucutre(structure_name, structure_type, arch_style, year_built, arch_firm, architect_name, street_address, city, state_or_province, postal_code, country, img_url):
    """Create and return a new architectural structure."""

    arch_structure = ArchitecturalStructure(
                                structure_name=structure_name,
                                structure_type=structure_type,
                                arch_style=arch_style, 
                                year_built=year_built,
                                arch_firm=arch_firm,
                                architect_name=architect_name, 
                                street_address=street_address, 
                                city=city, 
                                state_or_province=state_or_province, 
                                postal_code=postal_code, 
                                country=country, 
                                img_url=img_url)

    return arch_structure


def create_album(album_id, user_id):
    """Create and return a new user-curated album."""

    album = Album(album_id=album_id, user_id=user_id)

    return album


def create_objective(objective_id, ojbective_description, objective_complete):
    """Create and return an objective for the user to complete."""

    objective = Objective(
                    objective_id=objective_id, 
                    ojbective_description=ojbective_description, 
                    objective_complete=objective_complete)

    return objective


def create_submission(submission_type, user_structure_name, user_structure_type, user_arch_style, user_year_built, user_arch_firm, user_architect_name, user_street_address, user_city, user_state_or_province, user_postal_code, user_country, user_img_url, submission_complete):
    """Allow the user to create a submission."""

    submission = Submission(
                    submission_type=submission_type,
                    user_structure_name=user_structure_name,
                    user_structure_type=user_structure_name,
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

    return submission


def get_users():

    return User.query.all()


def get_arch_structures():

    return ArchitecturalStructure.query.all()


def get_albums():

    return Album.query.all()


def get_objectives():

    return Objective.query.all()


def get_submissions():

    return Submission.query.all()


def get_user_by_id(user_id):

    return User.query.get(user_id)


def get_user_by_email(email):

    return User.query.filter(User.email == email).first()


def get_arch_structure_by_id(structure_id):

    return ArchitecturalStructure.query.get(structure_id)


def get_album_by_id(album_id):

    return Album.query.get(album_id)


def get_objective_by_id(objective_id):

    return Objective.query.get(objective_id)


def get_submission_by_id(submission_id):

    return Submission.query.get(submission_id)


#def like_structure():
    """Allow the user to 'like' an ArchitecturalStructure object."""


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
