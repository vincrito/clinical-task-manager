from flask import Blueprint, render_template, request, redirect, url_for, flash  # web helpers (templates, forms, redirects, messages)
from flask_login import login_user, logout_user, login_required                  # session helpers (log in/out, protect routes)
from models import db                                                            # database session (for inserts/commits)
from models.user import User                                                     # User model (to create/query users)
from models.list import TaskList                                                  # TaskList model (for default lists)

bp = Blueprint("auth", __name__)                                                 # define an "auth" blueprint

@bp.get("/login")                                                                # GET /auth/login shows the login form
def login():
    return render_template("auth_login.html")                                    # render login template

@bp.post("/login")                                                               # POST /auth/login processes the form
def login_post():
    username = request.form.get("username", "").strip()                          # read username from form; strip spaces
    password = request.form.get("password", "")                                  # read password from form

    user = User.query.filter_by(username=username).first()                       # look up user by username
    if not user or not user.check_password(password):                            # if user missing or password wrong
        flash("Invalid credentials", "danger")                                   # show error message (Bootstrap red)
        return redirect(url_for("auth.login"))                                   # redirect back to login

    login_user(user)                                                             # log the user in (sets session cookie)
    flash("Welcome back!", "success")                                            # success message (green)
    return redirect(url_for("main.index"))                                       # go to homepage

@bp.get("/register")                                                             # GET /auth/register shows the registration form
def register():
    return render_template("auth_register.html")                                  # render register template

@bp.post("/register")                                                            # POST /auth/register processes the form
def register_post():
    username = request.form.get("username", "").strip()                          # read username
    password = request.form.get("password", "")                                  # read password
    confirm  = request.form.get("confirm", "")                                   # read confirmation password

    # basic validation: presence and match
    if not username or not password:                                             # require both fields
        flash("Username and password are required.", "danger")                   # error message
        return redirect(url_for("auth.register"))                                # back to form
    if password != confirm:                                                      # ensure passwords match
        flash("Passwords do not match.", "danger")                               # show mismatch error
        return redirect(url_for("auth.register"))                                # back to form

    # uniqueness check
    if User.query.filter_by(username=username).first():                          # see if username already exists
        flash("Username already taken.", "danger")                               # error if duplicate
        return redirect(url_for("auth.register"))                                # back to form

    # create and persist the new user
    interests_raw = request.form.getlist("interests")                            # list of selected interest tags
    interests = ",".join(t.strip() for t in interests_raw if t.strip())          # comma-separated string

    user = User(username=username, interests=interests)                          # create user object
    user.set_password(password)                                                  # hash and store password
    db.session.add(user)                                                         # stage user for insert
    db.session.flush()                                                           # get user.id before commit

    # create default lists for every new user
    for list_name in ("Personal", "Work"):
        db.session.add(TaskList(user_id=user.id, name=list_name))

    db.session.commit()                                                          # commit to the database

    flash("Account created. Please log in.", "success")                          # confirmation message
    return redirect(url_for("auth.login"))                                       # go to login page

@bp.post("/logout")                                                              # POST /auth/logout logs out the user
@login_required                                                                   # only logged-in users can log out
def logout():
    logout_user()                                                                 # clear user session
    flash("Logged out.", "success")                                               # confirmation message
    return redirect(url_for("auth.login"))                                        # back to login
