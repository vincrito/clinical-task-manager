from flask_sqlalchemy import SQLAlchemy  # import SQLAlchemy class to manage our DB

db = SQLAlchemy()                        # create a single DB object to be shared by models
