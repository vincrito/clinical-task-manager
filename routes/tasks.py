from flask import Blueprint, render_template, request, redirect, url_for, flash   # templates, forms, redirects, alerts
from flask_login import login_required, current_user                              # route protection and current user info
from models import db                                                             # database session for commits
from models.task import Task, ALLOWED_STATUSES                                    # Task model and allowed status values
from models.patient import Patient                                                # Patient model (for dropdowns/labels)
from models.comment import Comment                                                # Comment model (to read/write comments)            # import
from sqlalchemy import or_                                                        # optional SQL helper (not strictly needed)        # import
import re                                                                       # regular expressions for simple date validation  # import re
from datetime import datetime, date                                                   # robust date parsing/formatting

bp = Blueprint("tasks", __name__)                                                 # define the "tasks" blueprint

@bp.get("/tasks")                                                            # GET /tasks shows list                           # route
@login_required                                                              # must be logged in                               # guard
def list_tasks():
    status = request.args.get("status", "").strip()                          # optional ?status=                               # read
    q = request.args.get("q", "").strip()                                    # optional ?q=                                    # read
    patient_id = request.args.get("patient_id", "").strip()                  # optional ?patient_id=                           # read

    query = Task.query.filter_by(user_id=current_user.id)                    # only my tasks                                   # base

    if status and status in ALLOWED_STATUSES:                                # validate status filter                           # check
        query = query.filter(Task.status == status)                          # apply                                           # filter

    if patient_id.isdigit():                                                 # numeric patient id?                             # check
        query = query.filter(Task.patient_id == int(patient_id))             # apply                                           # filter

    if q:                                                                    # text search provided?                            # check
        like = f"%{q}%"                                                      # SQL LIKE pattern                                 # pattern
        query = query.filter(Task.description.ilike(like))                   # search description                               # filter

    rows = (query.order_by(                                                  # build ordering                                    # order
                Task.due_date.asc().nulls_last(),                            # earliest due first                                # order
                Task.created_at.desc())                                      # then newest created                               # tie-break
            .all())                                                          # run                                               # exec

    # map patient_id -> label for display
    patient_ids = {t.patient_id for t in rows}                               # collect unique patient ids                        # set
    patients = {}                                                            # id -> label map                                   # dict
    if patient_ids:                                                          # only query if needed                              # guard
        plist = (Patient.query
                 .filter(Patient.id.in_(patient_ids),
                         Patient.user_id == current_user.id)
                 .all())
        for p in plist:
            patients[p.id] = p.display_label()

    # load comments for all listed tasks in one query and group them
    task_ids = [t.id for t in rows]                                          # collect task ids                                  # list
    comments_by_task = {tid: [] for tid in task_ids}                         # init map id -> list                               # dict
    if task_ids:                                                             # only query if we have tasks                       # guard
        all_comments = (Comment.query
                        .filter(Comment.task_id.in_(task_ids))               # only comments for shown tasks                      # filter
                        .order_by(Comment.created_at.desc())                 # newest first                                       # order
                        .all())
        for c in all_comments:                                               # group comments by task id                          # loop
            comments_by_task[c.task_id].append(c)

    return render_template("tasks_list.html",                                 # render template                                    # render
                           tasks=rows,                                        # pass tasks                                          # ctx
                           patients=patients,                                 # pass patient labels                                 # ctx
                           comments_by_task=comments_by_task,                 # pass grouped comments                               # ctx
                           status=status, q=q, patient_id=patient_id)         # echo filters                                        # ctx


@bp.get("/tasks/new")                                                             # show the new task form                                                  # route
@login_required                                                                     # must be logged in                                                       # guard
def new_task():
    pre_pid = request.args.get("patient_id", "").strip()                           # optional ?patient_id= to preselect                                      # read
    patients = (Patient.query                                                      # query my patients for dropdown                                         # query
                .filter_by(user_id=current_user.id)                                # only my roster                                                          # scope
                .order_by(Patient.last_name.asc(), Patient.first_name.asc())       # sort by name                                                            # order
                .all())                                                            # run query                                                               # exec
    return render_template("tasks_new.html", patients=patients, pre_pid=pre_pid)   # render form + pass preselected id (if any)                              # render


@bp.post("/tasks/new")                                                            # POST /tasks/new handles creation
@login_required                                                                    # must be logged in
def create_task():
    description = request.form.get("description", "").strip()                     # task description from form
    due_date_raw = request.form.get("due_date", "").strip()                     # raw value from form (calendar or typed)
    due_date = None                                                             # default to None (no date)

    if due_date_raw:                                                            # if user provided a value
        parsed = None                                                           # holder for a successful parse
        for fmt in ("%Y-%m-%d", "%m/%d/%y", "%m/%d/%Y"):                        # try ISO (calendar), then MM/DD/YY, MM/DD/YYYY
            try:
                parsed = datetime.strptime(due_date_raw, fmt)                   # attempt to parse with this format
                break                                                           # stop on first success
            except ValueError:
                pass                                                            # try next format
        if not parsed:                                                          # none matched → invalid
            flash("Due date must be MM/DD/YY (or pick from the calendar).", "danger")  # show error
            return redirect(url_for("tasks.new_task"))                          # back to form
            
            # reject past dates (compare by date only)                                              # comment
        if parsed.date() < date.today():                                                        # past?
            flash("Due date cannot be in the past.", "danger")                                 # error
            return redirect(url_for("tasks.new_task"))                                          # back

        due_date = parsed.strftime("%Y-%m-%d")                                  # store normalized ISO for DB/sorting

    patient_id = request.form.get("patient_id", "").strip()                       # chosen patient id

    if not description:                                                           # validate required description
        flash("Description is required.", "danger")                               # show error
        return redirect(url_for("tasks.new_task"))                                # back to form

    if not patient_id.isdigit():                                                  # validate a numeric patient id
        flash("Select a valid patient.", "danger")                                # show error
        return redirect(url_for("tasks.new_task"))                                # back to form

    patient = (Patient.query
               .filter_by(id=int(patient_id), user_id=current_user.id)            # enforce ownership
               .first())
    if not patient:                                                               # if not found / not owned
        flash("Patient not found.", "danger")                                     # show error
        return redirect(url_for("tasks.new_task"))                                # back to form

    t = Task(user_id=current_user.id,                                             # create a new Task row
             patient_id=patient.id,                                               # link to the selected patient
             description=description,                                             # set description
             due_date=due_date,                                                   # must provide due date
             status="pending")                                                    # default status
    db.session.add(t)                                                             # stage the insert
    db.session.commit()                                                           # commit to DB
    flash("Task created.", "success")                                             # success message
    return redirect(url_for("tasks.list_tasks"))                                  # go back to the list

@bp.post("/tasks/<int:tid>/status")                                  # handle POST /tasks/<id>/status to change status       # route
@login_required                                                       # only logged-in users can do this                      # guard
def set_status(tid: int):
    new_status = request.form.get("status", "").strip()              # read the requested status from the form               # read form
    if new_status not in ALLOWED_STATUSES:                           # validate against allowed statuses                     # validate
        flash("Bad status.", "danger")                               # show error if invalid                                 # alert
        return redirect(url_for("tasks.list_tasks"))                 # return to the tasks list                              # redirect

    t = Task.query.filter_by(id=tid, user_id=current_user.id).first()# fetch the task, enforcing ownership                   # query
    if not t:                                                        # if no such task or not owned                          # check
        flash("Task not found.", "danger")                           # show error                                            # alert
        return redirect(url_for("tasks.list_tasks"))                 # back to list                                          # redirect

    t.status = new_status                                            # set the new status                                    # update
    db.session.commit()                                              # persist to database                                   # commit
    flash("Status updated.", "success")                              # success message                                       # alert
    return redirect(url_for("tasks.list_tasks"))                     # back to list                                          # redirect

@bp.post("/tasks/<int:tid>/comments")                                       # handle adding a comment to a task                    # route
@login_required                                                              # must be logged in                                    # guard
def add_comment(tid: int):
    body = request.form.get("body", "").strip()                              # comment text from form                               # read
    if not body:                                                             # validate non-empty                                   # check
        flash("Comment cannot be empty.", "danger")                          # show error                                           # alert
        return redirect(url_for("tasks.list_tasks"))                         # back to list                                         # redirect

    task = Task.query.filter_by(id=tid, user_id=current_user.id).first()     # enforce ownership                                    # query
    if not task:                                                             # task missing or not mine                             # check
        flash("Task not found.", "danger")                                   # error                                                # alert
        return redirect(url_for("tasks.list_tasks"))                         # back                                                 # redirect

    c = Comment(task_id=tid, user_id=current_user.id, body=body)             # build Comment row                                    # create
    db.session.add(c)                                                        # stage insert                                         # db
    db.session.commit()                                                      # commit                                               # db
    flash("Comment added.", "success")                                       # success message                                      # alert
    return redirect(url_for("tasks.list_tasks"))                             # back to the list                                     # redirect

@bp.post("/tasks/<int:tid>/delete")
@login_required
def delete_task(tid: int):
    t = Task.query.filter_by(id=tid, user_id=current_user.id).first()   # fetch task owned by user
    if not t:
        flash("Task not found.", "danger")
        return redirect(url_for("tasks.list_tasks"))

    # remove all comments tied to this task to avoid orphaned comments and ID reuse issues
    Comment.query.filter_by(task_id=t.id, user_id=current_user.id).delete(synchronize_session=False)  # bulk delete comments
    db.session.delete(t)                                                      # delete the task
    db.session.commit()                                                       # commit both deletions

    flash("Task deleted.", "success")
    return redirect(url_for("tasks.list_tasks"))

from datetime import datetime                               # we’ll reuse for date parsing                                # import

@bp.get("/tasks/<int:tid>/edit")                            # serve the edit form for a task                              # route
@login_required                                             # only logged-in users                                         # guard
def edit_task(tid: int):
    t = Task.query.filter_by(id=tid, user_id=current_user.id).first()  # fetch task that belongs to current user           # query
    if not t:                                               # if task not found or not owned                              # check
        flash("Task not found.", "danger")                  # show error                                                  # alert
        return redirect(url_for("tasks.list_tasks"))        # back to list                                                # redirect
    patients = (Patient.query                               # load patient choices for dropdown                           # query
                .filter_by(user_id=current_user.id)         # only my roster                                              # scope
                .order_by(Patient.last_name.asc(), Patient.first_name.asc())  # sort by name                               # order
                .all())                                     # execute query                                               # exec
    return render_template("tasks_edit.html", task=t, patients=patients)  # render edit form with current values           # render

@bp.post("/tasks/<int:tid>/edit")                           # process the edit form submission                            # route
@login_required                                             # only logged-in users                                         # guard
def update_task(tid: int):
    t = Task.query.filter_by(id=tid, user_id=current_user.id).first()  # fetch task enforcing ownership                   # query
    if not t:                                               # missing/not owned                                           # check
        flash("Task not found.", "danger")                  # error                                                       # alert
        return redirect(url_for("tasks.list_tasks"))        # back to list                                                # redirect

    description = request.form.get("description", "").strip()  # new description from form                               # read
    due_date_raw = request.form.get("due_date", "").strip()    # new due date (calendar or typed)                        # read
    patient_id = request.form.get("patient_id", "").strip()    # new patient id                                          # read
    status = request.form.get("status", "").strip()            # new status                                              # read

    if not description:                                    # ensure description present                                   # validate
        flash("Description is required.", "danger")        # error                                                       # alert
        return redirect(url_for("tasks.edit_task", tid=tid))   # back to edit                                            # redirect

    if not patient_id.isdigit():                           # ensure patient id is numeric                                 # validate
        flash("Select a valid patient.", "danger")         # error                                                       # alert
        return redirect(url_for("tasks.edit_task", tid=tid))   # back to edit                                            # redirect

    if status not in ALLOWED_STATUSES:                     # ensure status is allowed                                     # validate
        flash("Bad status.", "danger")                     # error                                                       # alert
        return redirect(url_for("tasks.edit_task", tid=tid))   # back to edit                                            # redirect

    # normalize due date: accept ISO (YYYY-MM-DD), MM/DD/YY, or MM/DD/YYYY; store as ISO or None
    due_date = None                                        # default                                                     # init
    if due_date_raw:                                       # if provided                                                  # check
        parsed = None                                      # holder for successful parse                                  # init
        for fmt in ("%Y-%m-%d", "%m/%d/%y", "%m/%d/%Y"):   # try supported formats                                        # loop
            try:
                parsed = datetime.strptime(due_date_raw, fmt)  # parse candidate                                         # parse
                break                                       # stop on success                                             # break
            except ValueError:
                pass                                        # try next format                                             # continue
        if not parsed:                                     # none matched                                                 # check
            flash("Due date must be MM/DD/YY (or use the calendar).", "danger")  # error                                # alert
            return redirect(url_for("tasks.edit_task", tid=tid))  # back to edit                                         # redirect
            # reject past dates                                                                      # comment
        if parsed.date() < date.today():                                                         # past?
            flash("Due date cannot be in the past.", "danger")                                  # error
            return redirect(url_for("tasks.edit_task", tid=tid))                                 # back

        due_date = parsed.strftime("%Y-%m-%d")             # store normalized ISO                                         # normalize

    # verify the selected patient belongs to the user
    patient = Patient.query.filter_by(id=int(patient_id), user_id=current_user.id).first()  # ownership check            # query
    if not patient:                                       # not found/not owned                                          # check
        flash("Patient not found.", "danger")             # error                                                        # alert
        return redirect(url_for("tasks.edit_task", tid=tid))  # back                                                     # redirect

    # apply updates
    t.description = description                           # set description                                              # update
    t.due_date = due_date                                 # set due date (ISO or None)                                   # update
    t.patient_id = patient.id                             # set patient link                                             # update
    t.status = status                                     # set status                                                   # update
    db.session.commit()                                   # save changes                                                 # commit

    flash("Task updated.", "success")                     # success message                                              # alert
    return redirect(url_for("tasks.list_tasks"))          # back to list                                                 # redirect
