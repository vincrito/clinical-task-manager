from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db
from models.task import Task, ALLOWED_STATUSES, ALLOWED_PRIORITIES
from models.list import TaskList
from models.comment import Comment
from sqlalchemy import or_
import re
from datetime import datetime
from zoneinfo import ZoneInfo

EASTERN = ZoneInfo("America/New_York")

bp = Blueprint("tasks", __name__)

@bp.post("/tasks/quick-add")
@login_required
def quick_add():
    """JSON endpoint used by the dashboard quick-add modal."""
    description = request.form.get("description", "").strip()
    due_date_raw = request.form.get("due_date", "").strip()
    list_id = request.form.get("list_id", "").strip()
    priority = request.form.get("priority", "medium").strip()

    if not description:
        return jsonify(ok=False, error="Description is required.")
    if not list_id.isdigit():
        return jsonify(ok=False, error="Invalid list.")
    lst = TaskList.query.filter_by(id=int(list_id), user_id=current_user.id).first()
    if not lst:
        return jsonify(ok=False, error="List not found.")
    if priority not in ALLOWED_PRIORITIES:
        priority = "medium"

    today_eastern = datetime.now(EASTERN).date()
    due_date = None
    if due_date_raw:
        parsed = None
        for fmt in ("%Y-%m-%d", "%m/%d/%y", "%m/%d/%Y"):
            try:
                parsed = datetime.strptime(due_date_raw, fmt)
                break
            except ValueError:
                pass
        if not parsed:
            return jsonify(ok=False, error="Invalid due date format.")
        if parsed.date() < today_eastern:
            return jsonify(ok=False, error="Due date cannot be in the past.")
        due_date = parsed.strftime("%Y-%m-%d")

    # No due date → auto low priority
    if not due_date:
        priority = "low"

    t = Task(user_id=current_user.id, list_id=lst.id,
             description=description, due_date=due_date,
             status="pending", priority=priority)
    db.session.add(t)
    db.session.commit()
    return jsonify(ok=True, task_id=t.id, list_id=lst.id,
                   description=description, due_date=due_date or "",
                   priority=priority)

@bp.post("/tasks/<int:tid>/complete-json")
@login_required
def complete_json(tid: int):
    t = Task.query.filter_by(id=tid, user_id=current_user.id).first()
    if not t:
        return jsonify(ok=False, error="Task not found.")
    t.status = "completed"
    db.session.commit()
    return jsonify(ok=True, task_id=tid)

@bp.get("/tasks/<int:tid>/json")
@login_required
def task_json(tid: int):
    t = Task.query.filter_by(id=tid, user_id=current_user.id).first()
    if not t:
        return jsonify(ok=False, error="Not found.")
    comments = (Comment.query
                .filter_by(task_id=tid)
                .order_by(Comment.created_at.asc())
                .all())
    lists = (TaskList.query
             .filter_by(user_id=current_user.id)
             .order_by(TaskList.name.asc())
             .all())
    return jsonify(
        ok=True,
        task={
            "id": t.id,
            "description": t.description,
            "due_date": t.due_date or "",
            "status": t.status,
            "priority": t.priority,
            "list_id": t.list_id,
        },
        comments=[{
            "body": c.body,
            "created_at": c.created_at.strftime("%m/%d/%y %I:%M%p") if c.created_at else "",
        } for c in comments],
        lists=[{"id": l.id, "name": l.name} for l in lists],
    )

@bp.post("/tasks/<int:tid>/update-json")
@login_required
def update_json(tid: int):
    t = Task.query.filter_by(id=tid, user_id=current_user.id).first()
    if not t:
        return jsonify(ok=False, error="Not found.")
    description = request.form.get("description", "").strip()
    due_date_raw = request.form.get("due_date", "").strip()
    list_id = request.form.get("list_id", "").strip()
    status = request.form.get("status", "").strip()
    priority = request.form.get("priority", "medium").strip()
    if not description:
        return jsonify(ok=False, error="Description is required.")
    if status not in ALLOWED_STATUSES:
        status = t.status
    if priority not in ALLOWED_PRIORITIES:
        priority = t.priority
    due_date = None
    if due_date_raw:
        for fmt in ("%Y-%m-%d", "%m/%d/%y", "%m/%d/%Y"):
            try:
                due_date = datetime.strptime(due_date_raw, fmt).strftime("%Y-%m-%d")
                break
            except ValueError:
                pass
    if list_id.isdigit():
        lst = TaskList.query.filter_by(id=int(list_id), user_id=current_user.id).first()
        if lst:
            t.list_id = lst.id
    t.description = description
    t.due_date = due_date
    t.status = status
    t.priority = priority
    db.session.commit()
    return jsonify(ok=True)

@bp.post("/tasks/<int:tid>/comment-json")
@login_required
def comment_json(tid: int):
    t = Task.query.filter_by(id=tid, user_id=current_user.id).first()
    if not t:
        return jsonify(ok=False, error="Not found.")
    body = request.form.get("body", "").strip()
    if not body:
        return jsonify(ok=False, error="Comment cannot be empty.")
    c = Comment(task_id=tid, user_id=current_user.id, body=body)
    db.session.add(c)
    db.session.commit()
    return jsonify(ok=True, comment={
        "body": c.body,
        "created_at": c.created_at.strftime("%m/%d/%y %I:%M%p") if c.created_at else "",
    })

@bp.get("/tasks/suggestions-json")
@login_required
def suggestions_json():
    """Return up to 50 recent distinct task descriptions for datalist autocomplete."""
    rows = (
        db.session.query(Task.description)
        .filter(Task.user_id == current_user.id)
        .order_by(Task.created_at.desc())
        .limit(200)
        .all()
    )
    seen = set()
    suggestions = []
    for (desc,) in rows:
        key = desc.lower()
        if key not in seen:
            seen.add(key)
            suggestions.append(desc)
        if len(suggestions) >= 50:
            break
    return jsonify(ok=True, suggestions=suggestions)

@bp.get("/tasks")
@login_required
def list_tasks():
    status = request.args.get("status", "").strip()
    q = request.args.get("q", "").strip()
    list_id = request.args.get("list_id", "").strip()
    priority = request.args.get("priority", "").strip()

    query = Task.query.filter_by(user_id=current_user.id)

    if status and status in ALLOWED_STATUSES:
        query = query.filter(Task.status == status)

    if priority and priority in ALLOWED_PRIORITIES:
        query = query.filter(Task.priority == priority)

    if list_id.isdigit():
        query = query.filter(Task.list_id == int(list_id))

    if q:                                                                    # text search provided?                            # check
        like = f"%{q}%"                                                      # SQL LIKE pattern                                 # pattern
        query = query.filter(Task.description.ilike(like))                   # search description                               # filter

    from sqlalchemy import case as _sa_case
    _pri = _sa_case(
        (Task.priority == "high", 1),
        (Task.priority == "medium", 2),
        else_=3
    )
    all_rows = (query.order_by(
                Task.due_date.asc().nulls_last(),
                _pri,
                Task.list_id)
            .all())

    active_tasks = [t for t in all_rows if t.status != "completed"]
    completed_tasks = sorted(
        [t for t in all_rows if t.status == "completed"],
        key=lambda t: t.updated_at or t.created_at,
        reverse=True,
    )

    # map list_id -> label for display
    all_rows = active_tasks + completed_tasks
    list_ids = {t.list_id for t in all_rows}
    lists = {}
    if list_ids:
        llist = (TaskList.query
                 .filter(TaskList.id.in_(list_ids),
                         TaskList.user_id == current_user.id)
                 .all())
        for l in llist:
            lists[l.id] = l.display_label()

    # load comments for all listed tasks in one query and group them
    task_ids = [t.id for t in all_rows]                                          # collect task ids                                  # list
    comments_by_task = {tid: [] for tid in task_ids}                         # init map id -> list                               # dict
    if task_ids:                                                             # only query if we have tasks                       # guard
        all_comments = (Comment.query
                        .filter(Comment.task_id.in_(task_ids))               # only comments for shown tasks                      # filter
                        .order_by(Comment.created_at.desc())                 # newest first                                       # order
                        .all())
        for c in all_comments:                                               # group comments by task id                          # loop
            comments_by_task[c.task_id].append(c)

    all_user_lists = (TaskList.query
                      .filter_by(user_id=current_user.id)
                      .order_by(TaskList.name.asc())
                      .all())
    list_colors = {l.id: l.color for l in all_user_lists}

    comment_counts = {tid: len(cs) for tid, cs in comments_by_task.items()}
    comment_latest = {tid: cs[0].body if cs else "" for tid, cs in comments_by_task.items()}

    return render_template("tasks_list.html",
                           active_tasks=active_tasks,
                           completed_tasks=completed_tasks,
                           lists=lists,
                           all_user_lists=all_user_lists,
                           list_colors=list_colors,
                           comment_counts=comment_counts,
                           comment_latest=comment_latest,
                           status=status, q=q, list_id=list_id,
                           priority=priority)


@bp.get("/tasks/new")                                                             # show the new task form                                                  # route
@login_required                                                                     # must be logged in                                                       # guard
def new_task():
    pre_lid = request.args.get("list_id", "").strip()
    lists = (TaskList.query
             .filter_by(user_id=current_user.id)
             .order_by(TaskList.name.asc())
             .all())
    return render_template("tasks_new.html", lists=lists, pre_lid=pre_lid)


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

    list_id = request.form.get("list_id", "").strip()

    if not description:
        flash("Description is required.", "danger")
        return redirect(url_for("tasks.new_task"))

    if not list_id.isdigit():
        flash("Select a valid list.", "danger")
        return redirect(url_for("tasks.new_task"))

    lst = (TaskList.query
           .filter_by(id=int(list_id), user_id=current_user.id)
           .first())
    if not lst:
        flash("List not found.", "danger")
        return redirect(url_for("tasks.new_task"))

    priority = request.form.get("priority", "medium").strip()
    if priority not in ALLOWED_PRIORITIES:
        priority = "medium"

    t = Task(user_id=current_user.id,
             list_id=lst.id,
             description=description,
             due_date=due_date,
             status="pending",
             priority=priority)
    db.session.add(t)                                                             # stage the insert
    db.session.commit()                                                           # commit to DB
    flash("Task created.", "success")                                             # success message
    redirect_to = request.form.get("redirect_to", "").strip()
    if redirect_to and redirect_to.startswith("/") and not redirect_to.startswith("//"):
        return redirect(redirect_to)
    return redirect(url_for("tasks.list_tasks"))                                  # go back to the list

@bp.post("/tasks/<int:tid>/status")
@login_required
def set_status(tid: int):
    new_status = request.form.get("status", "").strip()
    if new_status not in ALLOWED_STATUSES:
        flash("Bad status.", "danger")
        return redirect(url_for("tasks.list_tasks"))
    t = Task.query.filter_by(id=tid, user_id=current_user.id).first()
    if not t:
        flash("Task not found.", "danger")
        return redirect(url_for("tasks.list_tasks"))
    t.status = new_status
    db.session.commit()
    flash("Status updated.", "success")
    # honour redirect_to for list detail page
    redirect_to = request.form.get("redirect_to", "").strip()
    if redirect_to and redirect_to.startswith("/") and not redirect_to.startswith("//"):
        return redirect(redirect_to)
    return redirect(url_for("tasks.list_tasks"))

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

    Comment.query.filter_by(task_id=t.id, user_id=current_user.id).delete(synchronize_session=False)
    db.session.delete(t)
    db.session.commit()
    flash("Task deleted.", "success")
    redirect_to = request.form.get("redirect_to", "").strip()
    if redirect_to and redirect_to.startswith("/") and not redirect_to.startswith("//"):
        return redirect(redirect_to)
    return redirect(url_for("tasks.list_tasks"))

from datetime import datetime                               # we’ll reuse for date parsing                                # import

@bp.get("/tasks/<int:tid>/edit")                            # serve the edit form for a task                              # route
@login_required                                             # only logged-in users                                         # guard
def edit_task(tid: int):
    t = Task.query.filter_by(id=tid, user_id=current_user.id).first()  # fetch task that belongs to current user           # query
    if not t:                                               # if task not found or not owned                              # check
        flash("Task not found.", "danger")                  # show error                                                  # alert
        return redirect(url_for("tasks.list_tasks"))        # back to list                                                # redirect
    lists = (TaskList.query
             .filter_by(user_id=current_user.id)
             .order_by(TaskList.name.asc())
             .all())
    return render_template("tasks_edit.html", task=t, lists=lists)

@bp.post("/tasks/<int:tid>/edit")                           # process the edit form submission                            # route
@login_required                                             # only logged-in users                                         # guard
def update_task(tid: int):
    t = Task.query.filter_by(id=tid, user_id=current_user.id).first()  # fetch task enforcing ownership                   # query
    if not t:                                               # missing/not owned                                           # check
        flash("Task not found.", "danger")                  # error                                                       # alert
        return redirect(url_for("tasks.list_tasks"))        # back to list                                                # redirect

    description = request.form.get("description", "").strip()
    due_date_raw = request.form.get("due_date", "").strip()
    list_id = request.form.get("list_id", "").strip()
    status = request.form.get("status", "").strip()

    if not description:
        flash("Description is required.", "danger")
        return redirect(url_for("tasks.edit_task", tid=tid))

    if not list_id.isdigit():
        flash("Select a valid list.", "danger")
        return redirect(url_for("tasks.edit_task", tid=tid))

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

    # verify the selected list belongs to the user
    lst = TaskList.query.filter_by(id=int(list_id), user_id=current_user.id).first()
    if not lst:
        flash("List not found.", "danger")
        return redirect(url_for("tasks.edit_task", tid=tid))

    priority = request.form.get("priority", "medium").strip()
    if priority not in ALLOWED_PRIORITIES:
        priority = "medium"

    # apply updates
    t.description = description
    t.due_date = due_date
    t.list_id = lst.id
    t.status = status
    t.priority = priority
    db.session.commit()                                   # save changes                                                 # commit

    flash("Task updated.", "success")                     # success message                                              # alert
    return redirect(url_for("tasks.list_tasks"))          # back to list                                                 # redirect
