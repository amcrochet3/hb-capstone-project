"""CRUD Operations"""

from model import db, ArchitecturalStructure, User, Like, Album, Objective, Submission, connect_to_db, ObjectiveSubmission

def create_user(fname, lname, email, password):
    """Create and return a new user."""

    user = User(fname=fname, lname=lname, email=email, password=password)

    return user


def create_arch_structure(user_id, structure_name, structure_type, arch_style, year_built, arch_firm, architect_name, street_address, city, state_or_province, postal_code, country, arch_img_file_path, lat, lng):
    """Create and return a new architectural structure."""

    arch_structure = ArchitecturalStructure(
                                user_id=user_id,
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
                                arch_img_file_path=arch_img_file_path,
                                lat=lat,
                                lng=lng)

    db.session.add(arch_structure)
    db.session.commit()

    return arch_structure


def create_album(user_id, album_name):
    """Create a new album and return the album object."""

    user = User.query.get(user_id)
    album = Album(user=user, album_name=album_name)
    db.session.add(album)
    db.session.commit()

    return album


def create_objective(objective_id, objective_description):
    """Create and return an objective for the user to complete."""

    objective = Objective(
                    objective_id=objective_id, 
                    objective_description=objective_description)

    return objective


def create_db_submission(user_id, submission_type, user_structure_name, user_structure_type, user_arch_style, user_year_built, user_arch_firm, user_architect_name, user_street_address, user_city, user_state_or_province, user_postal_code, user_country, db_upload_file_path):
    """Allow the user to create a submission."""

    submission = Submission(
                    user_id=user_id,
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
                    db_upload_file_path=db_upload_file_path,
                )

    db.session.add(submission)
    db.session.commit()

    return submission


def create_obj_submission(user_id, submission_type, objective_description, obj_upload_file_path):

    submission = Submission(
                    user_id=user_id,
                    submission_type=submission_type,
                    objective_description=objective_description,
                    obj_upload_file_path=obj_upload_file_path,
                )

    db.session.add(submission)
    db.session.commit()

    return submission



def create_obj_sub(objective_id, submission_id):
    """Creates an ObjectiveSubmission object using an Objective object's id and a Submission object's id"""

    new_obj_sub = ObjectiveSubmission(objective_id=objective_id, submission_id=submission_id)

    db.session.add(new_obj_sub)
    db.session.commit()

    return new_obj_sub


# def create_objsub(objective, submission):
#     """Creates an ObjectiveSubmission object using an Objective object and a Submission object.
#     This creates a relationship between said Objective and said Object"""

#     new_obj_sub = ObjectiveSubmission(objective=objective, submission=submission)

#     db.session.add(new_obj_sub)
#     db.session.commit()

#     return new_obj_sub


def get_users():

    return User.query.all()


def get_arch_structures():
    
    return ArchitecturalStructure.query.order_by(ArchitecturalStructure.structure_id.asc())


def get_albums():

    return Album.query.all()


def get_objectives():

    return Objective.query.all()


def get_submissions():

    return Submission.query.all()


def get_user_by_id(user_id):

    return User.query.filter(User.user_id == user_id).first()


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


def get_albums_by_user_id(user_id):
    
    return Album.query.filter_by(user_id=user_id).all()


def add_structure_to_album(album_id, structure_id):
    """Add a structure to an album."""

    structure = ArchitecturalStructure.query.get(structure_id)
    album = Album.query.get(album_id)

    album.structures.append(structure)

    db.session.add(album)
    db.session.commit()

    return album



if __name__ == '__main__':
    from server import app
    connect_to_db(app)
