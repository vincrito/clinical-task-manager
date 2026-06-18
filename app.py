import os                                                # read env vars and build file paths
from flask import Flask                                  # Flask application class
from flask_login import LoginManager                     # handles user sessions
from models import db                                    # shared SQLAlchemy db object
from models.user import User, bcrypt                     # import User model and bcrypt instance
from datetime import datetime                         # used by the date formatting filter

login_manager = LoginManager()                           # create a LoginManager instance

def create_app():
    app = Flask(__name__, instance_relative_config=True) 
    # create the Flask app; use instance/ for private files like the SQLite DB

    @app.template_filter("mdy")                       # register a template filter named "mdy"
    def _fmt_mdy(date_str):                          # takes a YYYY-MM-DD string (or None)
        if not date_str:                              # empty/None guard
            return ""                                 # show nothing in the UI
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").strftime("%m/%d/%y")  # format to MM/DD/YY
        except Exception:
            return date_str                           # if something odd, fall back to raw

    @app.template_filter("statuslabel")                  # new template filter
    def _fmt_statuslabel(status):                        # takes raw status string
        mapping = {                                      # mapping from raw to nice label
            "pending": "Pending",
            "in_progress": "In Progress",
            "completed": "Completed"
        }
        return mapping.get(status, status)               # return mapped label, fallback raw

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
    # secret used to sign session cookies; read from env or fallback

    os.makedirs(app.instance_path, exist_ok=True)
    # ensure instance/ exists (where SQLite DB will live)

    instance_db_path = os.path.join(app.instance_path, "app.db")
    # build ABSOLUTE path to instance/app.db (prevents sqlite open errors)

    db_url = os.getenv("DATABASE_URL", f"sqlite:///{instance_db_path}")
    # Render provides postgres:// but SQLAlchemy 2.x requires postgresql://
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # turn off unneeded SQLAlchemy event system

    db.init_app(app)                                     # attach SQLAlchemy to this app
    bcrypt.init_app(app)                                 # attach Bcrypt (needed for password hashing)
    login_manager.init_app(app)                          # attach Flask-Login to this app
    login_manager.login_view = "auth.login"              # route name Flask-Login redirects to when login required

    from routes.main import bp as main_bp                # import the basic homepage blueprint
    app.register_blueprint(main_bp)                      # register it

    from routes.auth import bp as auth_bp                # import the auth blueprint (defined next)
    app.register_blueprint(auth_bp, url_prefix="/auth")  # register under /auth (so /auth/login, /auth/register)

    from routes.lists import bp as lists_bp
    app.register_blueprint(lists_bp)
    
    from routes.tasks import bp as tasks_bp
    app.register_blueprint(tasks_bp)

    from routes.articles import bp as articles_bp
    app.register_blueprint(articles_bp)

    from models.user import User
    from models.list import TaskList
    from models.task import Task
    from models.comment import Comment
    from models.article import Article, ArticleReaction

    @login_manager.user_loader
    def load_user(user_id: str):
        return User.query.get(int(user_id))

    @app.context_processor
    def inject_navbar_stats():
        from flask_login import current_user
        from sqlalchemy import func
        if not current_user.is_authenticated:
            return {"navbar_stats": None}
        rows = (
            db.session.query(Task.status, func.count(Task.id))
            .filter(Task.user_id == current_user.id)
            .group_by(Task.status)
            .all()
        )
        s = {"pending": 0, "in_progress": 0, "completed": 0}
        for status, cnt in rows:
            if status in s:
                s[status] = cnt
        return {"navbar_stats": s}

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
        # Add new columns to existing tables if they don't exist yet (SQLite migration)
        from sqlalchemy import text, inspect as sa_inspect
        insp = sa_inspect(db.engine)
        existing_article_cols = {c["name"] for c in insp.get_columns("articles")}
        if "content_type" not in existing_article_cols:
            with db.engine.connect() as conn:
                conn.execute(text("ALTER TABLE articles ADD COLUMN content_type VARCHAR(60) NOT NULL DEFAULT 'Article'"))
                conn.commit()
        existing_user_cols = {c["name"] for c in insp.get_columns("users")}
        if "interests" not in existing_user_cols:
            with db.engine.connect() as conn:
                conn.execute(text("ALTER TABLE users ADD COLUMN interests VARCHAR(500) NOT NULL DEFAULT ''"))
                conn.commit()
    app.run(host="127.0.0.1", port=8000, debug=True)     # run on port 8000
