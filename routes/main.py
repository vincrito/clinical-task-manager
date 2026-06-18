from flask import Blueprint, render_template, session
from flask_login import current_user
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

EASTERN = ZoneInfo("America/New_York")

bp = Blueprint("main", __name__)

@bp.get("/")
def index():
    article = None
    show_work_modal = False
    stats = None
    overdue = []
    due_today = []
    due_this_week = []
    open_tasks = []
    list_panels = []
    list_colors = {}
    list_names = {}
    comment_counts = {}
    comment_latest = {}
    _today_dt = datetime.now(EASTERN).date()
    today = _today_dt.isoformat()
    week_end = (_today_dt + timedelta(days=7)).isoformat()

    if current_user.is_authenticated:
        from routes.articles import get_featured_article
        from models.task import Task, ALLOWED_STATUSES
        from models.list import TaskList
        from models import db
        from sqlalchemy import func, case

        uid = current_user.id

        priority_order = case(
            (Task.priority == "high", 1),
            (Task.priority == "medium", 2),
            else_=3
        )

        # Summary counts grouped by status
        count_rows = (
            db.session.query(Task.status, func.count(Task.id))
            .filter(Task.user_id == uid)
            .group_by(Task.status)
            .all()
        )
        stats = {"pending": 0, "in_progress": 0, "completed": 0}
        for status, cnt in count_rows:
            if status in stats:
                stats[status] = cnt

        # Overdue: not completed, due_date < today — ordered by priority then due_date
        overdue = (
            Task.query
            .filter(
                Task.user_id == uid,
                Task.status != "completed",
                Task.due_date.isnot(None),
                Task.due_date < today,
            )
            .order_by(priority_order, Task.list_id, Task.due_date.asc())
            .all()
        )

        # Due today: not completed, due_date == today only
        due_today = (
            Task.query
            .filter(
                Task.user_id == uid,
                Task.status != "completed",
                Task.due_date == today,
            )
            .order_by(priority_order, Task.list_id)
            .all()
        )

        # Open Tasks: not completed, no due date
        open_tasks = (
            Task.query
            .filter(
                Task.user_id == uid,
                Task.status != "completed",
                Task.due_date.is_(None),
            )
            .order_by(priority_order, Task.list_id)
            .all()
        )

        # Due this week: not completed, due_date in (today+1 .. today+7)
        due_this_week = (
            Task.query
            .filter(
                Task.user_id == uid,
                Task.status != "completed",
                Task.due_date > today,
                Task.due_date <= week_end,
            )
            .order_by(priority_order, Task.due_date.asc(), Task.list_id)
            .all()
        )

        # Per-list panels
        lists = (
            TaskList.query
            .filter_by(user_id=uid)
            .order_by(TaskList.name.asc())
            .all()
        )

        # Build list_colors for task rows (int key → color string)
        list_colors = {l.id: l.color for l in lists}
        list_names = {l.id: l.name for l in lists}

        lc_rows = (
            db.session.query(Task.list_id, Task.status, func.count(Task.id))
            .filter(Task.user_id == uid)
            .group_by(Task.list_id, Task.status)
            .all()
        )
        lc_map = {}
        for lid, st, cnt in lc_rows:
            if lid not in lc_map:
                lc_map[lid] = {"pending": 0, "in_progress": 0, "completed": 0, "total": 0}
            if st in lc_map[lid]:
                lc_map[lid][st] = cnt
            lc_map[lid]["total"] += cnt

        for lst in lists:
            lc = lc_map.get(lst.id, {"pending": 0, "in_progress": 0, "completed": 0, "total": 0})
            total = lc["total"]
            pct = round(lc["completed"] / total * 100) if total else 0
            list_panels.append({
                "id": lst.id,
                "name": lst.name,
                "color": lst.color,
                "pending": lc["pending"],
                "in_progress": lc["in_progress"],
                "completed": lc["completed"],
                "total": total,
                "pct": pct,
            })

        article = get_featured_article(uid)
        show_work_modal = session.pop("show_work_modal", False)
        session.modified = True

        # Comment counts for dashboard task rows
        from models.comment import Comment
        all_dash_ids = [t.id for t in overdue + due_today + due_this_week + open_tasks]
        dash_cmap = {}
        if all_dash_ids:
            for c in Comment.query.filter(Comment.task_id.in_(all_dash_ids)).order_by(Comment.created_at.desc()).all():
                dash_cmap.setdefault(c.task_id, []).append(c)
        comment_counts = {tid: len(cs) for tid, cs in dash_cmap.items()}
        comment_latest = {tid: cs[0].body for tid, cs in dash_cmap.items()}

    return render_template(
        "index.html",
        article=article,
        show_work_modal=show_work_modal,
        stats=stats,
        overdue=overdue,
        due_today=due_today,
        due_this_week=due_this_week,
        open_tasks=open_tasks,
        list_panels=list_panels,
        list_colors=list_colors,
        list_names=list_names,
        comment_counts=comment_counts,
        comment_latest=comment_latest,
        today=today,
        week_end=week_end,
    )
