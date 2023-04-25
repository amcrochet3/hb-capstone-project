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
    city = db.Column(db.String(100))
    state_or_province = db.Column(db.String(50), nullable=True)
    postal_code = db.Column(db.String(10), nullable=True)
    country = db.Column(db.String(50))
    img_url = db.Column(db.String(255))

    likes = db.relationship("Like", back_populates="architectural_structure")

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
    album = db.relationship("Album", back_populates="user")


class Admin(db.Model):

    __tablename__ = "admins"

    admin_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), primary_key=True)

    user = db.relationship("User", back_populates="admin")


class Like(db.Model):

    __tablename__ = "likes"

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), primary_key=True)
    structure_id = db.Column(db.Integer, db.ForeignKey("architectural_structures.structure_id"))
    liked = db.Column(db.Boolean, nullable=True)

    user = db.relationship("User", back_populates="likes")
    architectural_structure = db.relationship("ArchitecturalStructure", back_populates="likes")


class Album(db.Model):

    __tablename__ = "albums"

    album_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    user = db.relationship("User", back_populates="album")


class Objective(db.Model):

    __tablename__ = "objectives"

    objective_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    ojbective_description = db.Column(db.String(255))
    objective_complete = db.Column(db.Boolean)


class Submission(db.Model):

    __tablename__ = "submissions"

    submission_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    submission_type = db.Column(db.String(25))
    user_id = db.Column(db.Integer)
    user_structure_name = db.Column(db.String(255), nullable=True)
    user_structure_type = db.Column(db.String(255))
    user_arch_style = db.Column(db.String(100))
    user_year_built = db.Column(db.Integer, nullable=True)
    user_arch_firm = db.Column(db.String(255), nullable=True)
    user_architect_name = db.Column(db.String(255), nullable=True)
    user_street_address = db.Column(db.String(255), nullable=True)
    user_city = db.Column(db.String(50))
    user_state_or_province = db.Column(db.String(50), nullable=True)
    user_postal_code = db.Column(db.Integer, nullable=True)
    user_country = db.Column(db.String(50))
    user_img_url = db.Column(db.String(255))
    submission_complete = db.Column(db.Boolean)


def connect_to_db(flask_app, db_uri="postgresql:///local_structure", echo=True):
    
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    
    from server import app
    connect_to_db(app)