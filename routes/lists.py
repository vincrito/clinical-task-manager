from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db
from models.list import TaskList, LIST_COLORS
from models.task import Task

bp = Blueprint("lists", __name__)

@bp.get("/lists")
@login_required
def list_lists():
    from sqlalchemy import func
    q = request.args.get("q", "").strip()
    base = TaskList.query.filter_by(user_id=current_user.id)
    if q:
        like = f"%{q}%"
        base = base.filter(TaskList.name.ilike(like))
    rows = base.order_by(TaskList.name.asc()).all()
    count_rows = (
        db.session.query(Task.list_id, Task.status, func.count(Task.id))
        .filter(Task.user_id == current_user.id)
        .group_by(Task.list_id, Task.status)
        .all()
    )
    lc_map = {}
    for lid, st, cnt in count_rows:
        if lid not in lc_map:
            lc_map[lid] = {"pending": 0, "in_progress": 0, "completed": 0, "total": 0}
        if st in lc_map[lid]:
            lc_map[lid][st] = cnt
        lc_map[lid]["total"] += cnt
    list_stats = {lst.id: lc_map.get(lst.id, {"pending": 0, "in_progress": 0, "completed": 0, "total": 0}) for lst in rows}
    return render_template("lists_list.html", lists=rows, q=q, list_stats=list_stats)

@bp.get("/lists/new")
@login_required
def new_list():
    return render_template("lists_new.html")

@bp.post("/lists/new")
@login_required
def create_list():
    name = request.form.get("name", "").strip()
    description = request.form.get("description", "").strip()
    if not name:
        flash("Name is required.", "danger")
        return redirect(url_for("lists.new_list"))
    lst = TaskList(user_id=current_user.id, name=name, description=description or None)
    db.session.add(lst)
    db.session.commit()
    flash("List created.", "success")
    return redirect(url_for("lists.list_lists"))

@bp.post("/lists/new-json")
@login_required
def create_list_json():
    """AJAX endpoint used by the dashboard New List modal."""
    name = request.form.get("name", "").strip()
    description = request.form.get("description", "").strip()
    if not name:
        return jsonify(ok=False, error="Name is required.")
    if TaskList.query.filter_by(user_id=current_user.id, name=name).first():
        return jsonify(ok=False, error="You already have a list with that name.")
    lst = TaskList(user_id=current_user.id, name=name, description=description or None)
    db.session.add(lst)
    db.session.commit()
    return jsonify(ok=True, list={
        "id": lst.id,
        "name": lst.name,
        "color": LIST_COLORS[(lst.id - 1) % len(LIST_COLORS)],
    })

@bp.get("/lists/<int:lid>")
@login_required
def list_detail(lid: int):
    lst = TaskList.query.filter_by(id=lid, user_id=current_user.id).first_or_404()
    from sqlalchemy import case as _sa_case
    from models.comment import Comment
    _pri = _sa_case(
        (Task.priority == "high", 1),
        (Task.priority == "medium", 2),
        else_=3
    )
    tasks = (Task.query
             .filter_by(user_id=current_user.id, list_id=lid)
             .order_by(Task.due_date.asc().nulls_last(), _pri)
             .all())
    all_lists = TaskList.query.filter_by(user_id=current_user.id).order_by(TaskList.name).all()
    list_colors = {l.id: l.color for l in all_lists}
    task_ids = [t.id for t in tasks]
    cmap = {}
    if task_ids:
        for c in Comment.query.filter(Comment.task_id.in_(task_ids)).order_by(Comment.created_at.desc()).all():
            cmap.setdefault(c.task_id, []).append(c)
    comment_counts = {tid: len(cs) for tid, cs in cmap.items()}
    comment_latest = {tid: cs[0].body for tid, cs in cmap.items()}
    return render_template("list_detail.html", lst=lst, tasks=tasks,
                           list_colors=list_colors,
                           comment_counts=comment_counts,
                           comment_latest=comment_latest)

@bp.get("/lists/<int:lid>/edit")
@login_required
def edit_list(lid: int):
    lst = TaskList.query.filter_by(id=lid, user_id=current_user.id).first_or_404()
    return render_template("lists_edit.html", lst=lst)

@bp.post("/lists/<int:lid>/edit")
@login_required
def update_list(lid: int):
    lst = TaskList.query.filter_by(id=lid, user_id=current_user.id).first_or_404()
    name = request.form.get("name", "").strip()
    description = request.form.get("description", "").strip()
    if not name:
        flash("Name is required.", "danger")
        return redirect(url_for("lists.edit_list", lid=lid))
    lst.name = name
    lst.description = description or None
    db.session.commit()
    flash("List updated.", "success")
    return redirect(url_for("lists.list_detail", lid=lid))

@bp.post("/lists/<int:lid>/delete")
@login_required
def delete_list(lid: int):
    lst = TaskList.query.filter_by(id=lid, user_id=current_user.id).first()
    if not lst:
        flash("List not found.", "danger")
        return redirect(url_for("lists.list_lists"))
    has_tasks = Task.query.filter_by(user_id=current_user.id, list_id=lid).first()
    if has_tasks:
        flash("Cannot delete: list has tasks. Delete or move tasks first.", "danger")
        return redirect(url_for("lists.list_detail", lid=lid))
    db.session.delete(lst)
    db.session.commit()
    flash("List deleted.", "success")
    return redirect(url_for("lists.list_lists"))
