from flask_login import UserMixin          # adds Flask-Login properties/methods         # import UserMixin
from datetime import datetime                           # timestamp helper
from zoneinfo import ZoneInfo                           # stdlib time zones (Py 3.9+)
EASTERN = ZoneInfo("America/New_York")                  # US/Eastern tz
from . import db                           # shared SQLAlchemy db object                  # import db
from flask_bcrypt import Bcrypt            # secure password hashing                      # import Bcrypt

bcrypt = Bcrypt()                          # create a Bcrypt helper we can use            # init bcrypt

class User(UserMixin, db.Model):           # SQLAlchemy model + Flask-Login mixin         # define User model
    __tablename__ = "users"                # explicit table name                          # set table name

    id = db.Column(db.Integer, primary_key=True)                         # primary key     # id column
    username = db.Column(db.String(80), unique=True, nullable=False)     # unique login    # username column
    password_hash = db.Column(db.String(255), nullable=False)            # hashed secret   # password_hash column
    interests = db.Column(db.String(500), nullable=False, default="")    # comma-sep interest tags selected at signup
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(EASTERN).replace(tzinfo=None))


    def set_password(self, password: str) -> None:                       # setter method   # define set_password
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        # hash the plain password and store as text                        # hash & store

    def check_password(self, password: str) -> bool:                     # verify method   # define check_password
        return bcrypt.check_password_hash(self.password_hash, password)
        # compare plain password with stored hash                          # verify hash

    def __repr__(self):                                                  # debug helper    # repr
        return f"<User {self.username}>"                                 # friendly print  # return string
