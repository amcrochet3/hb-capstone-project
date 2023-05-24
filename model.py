"""Models for architecture app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ArchitecturalStructure(db.Model):

    __tablename__ = "architectural_structures"

    structure_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    structure_name = db.Column(db.String(255), nullable=True)
    structure_type = db.Column(db.String(255))
    arch_style = db.Column(db.String(255), nullable=True)
    year_built = db.Column(db.Integer, nullable=True)
    arch_firm = db.Column(db.String(255), nullable=True)
    architect_name = db.Column(db.String(255), nullable=True)
    street_address = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(255))
    state_or_province = db.Column(db.String(50), nullable=True)
    postal_code = db.Column(db.String(10), nullable=True)
    country = db.Column(db.String(50))
    arch_img_file_path = db.Column(db.String(255))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    num_likes = db.Column(db.Integer, default=0)
    album_id = db.Column(db.Integer, db.ForeignKey("albums.album_id"))

    likes = db.relationship("Like", back_populates="architectural_structure")
    user = db.relationship("User", back_populates="architectural_structures")
    albums = db.relationship("Album", secondary="album_structures", back_populates="structures")

    def __repr__(self):
        return f"<ArchitecturalStructure structure_name={self.structure_name} arch_style={self.arch_style} architect_name={self.architect_name}"


class User(db.Model):
    
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    admin = db.relationship("Admin", back_populates="user")
    likes = db.relationship("Like", back_populates="user")
    albums = db.relationship("Album", back_populates="user")
    architectural_structures = db.relationship("ArchitecturalStructure", back_populates="user")
    submissions = db.relationship("Submission", back_populates="user")


class Admin(db.Model):

    __tablename__ = "admins"

    admin_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), primary_key=True)

    user = db.relationship("User", back_populates="admin")


class Like(db.Model):

    __tablename__ = "likes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    structure_id = db.Column(db.Integer, db.ForeignKey("architectural_structures.structure_id"))
    liked = db.Column(db.Boolean)

    user = db.relationship("User", back_populates="likes")
    architectural_structure = db.relationship("ArchitecturalStructure", back_populates="likes")


class Album(db.Model):

    __tablename__ = "albums"

    album_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    album_name = db.Column(db.String(255))

    user = db.relationship("User", back_populates="albums")
    structures = db.relationship("ArchitecturalStructure", secondary="album_structures", back_populates="albums")


class AlbumStructure(db.Model):

    __tablename__ = "album_structures"

    album_structures_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    album_id = db.Column(db.Integer, db.ForeignKey("albums.album_id"))
    structure_id = db.Column(db.Integer, db.ForeignKey("architectural_structures.structure_id"))


class Objective(db.Model):
    __tablename__ = "objectives"
    
    objective_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    objective_description = db.Column(db.String(255))
    
    submissions = db.relationship("Submission", secondary="objective_submissions", back_populates="objectives")


class ObjectiveSubmission(db.Model):
    __tablename__ = "objective_submissions"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    submission_id = db.Column(db.Integer, db.ForeignKey("submissions.submission_id"))
    objective_id = db.Column(db.Integer, db.ForeignKey("objectives.objective_id"))
    

class Submission(db.Model):
    __tablename__ = "submissions"

    submission_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    submission_type = db.Column(db.String(25))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    user_structure_name = db.Column(db.String(255), nullable=True)
    user_structure_type = db.Column(db.String(255))
    user_arch_style = db.Column(db.String(100))
    user_year_built = db.Column(db.Integer, nullable=True)
    user_arch_firm = db.Column(db.String(255), nullable=True)
    user_architect_name = db.Column(db.String(255), nullable=True)
    user_street_address = db.Column(db.String(255), nullable=True)
    user_city = db.Column(db.String(50))
    user_state_or_province = db.Column(db.String(50), nullable=True)
    user_postal_code = db.Column(db.String(10), nullable=True)
    user_country = db.Column(db.String(50))
    db_upload_file_path = db.Column(db.String(255))
    objective_id = db.Column(db.Integer)
    obj_upload_file_path = db.Column(db.String(255))
    objective_description = db.Column(db.String(255))
    status = db.Column(db.Boolean)

    objectives = db.relationship("Objective", secondary="objective_submissions", back_populates="submissions")
    user = db.relationship("User", back_populates="submissions")


def connect_to_db(flask_app, db_uri="postgresql:///local_structure", echo=False):
    
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    
    from server import app
    connect_to_db(app)