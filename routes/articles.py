from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from models import db
from models.article import Article, ArticleReaction
from models.task import Task
from datetime import date, timedelta

bp = Blueprint("articles", __name__)


def get_featured_article(user_id):
    """Return the highest-scored unread/unskipped article for this user.

    Scoring:
    - Each tag on a liked article gets +1 weight; disliked gives -0.5 (floor 0.1).
    - User's declared interests get a permanent +2 boost per matching tag.
    - Unseen tags default to 1.0.
    Session-skipped and permanently reacted articles are excluded.
    Skip tracking resets daily.
    """
    from models.user import User
    # Daily reset of skip tracking
    today = date.today().isoformat()
    if session.get("skip_date") != today:
        session["skip_date"] = today
        session["skip_count"] = 0
        session["skipped_ids"] = []
        session.modified = True

    # Permanently excluded: already liked or disliked
    reacted_ids = [
        r.article_id
        for r in ArticleReaction.query.filter_by(user_id=user_id).all()
    ]
    # Also exclude session skips
    excluded_ids = reacted_ids + list(session.get("skipped_ids", []))

    # Suggest only from the user's own articles
    query = Article.query.filter(Article.added_by == user_id)
    if excluded_ids:
        query = query.filter(~Article.id.in_(excluded_ids))
    candidates = query.all()

    if not candidates:
        return None

    # Build tag weight map from reaction history
    tag_weights = {}
    for r in ArticleReaction.query.filter_by(user_id=user_id).all():
        a = db.session.get(Article, r.article_id)
        if not a:
            continue
        delta = 1.0 if r.reaction == "liked" else -0.5
        for tag in a.tag_list():
            tag_weights[tag] = max(0.1, tag_weights.get(tag, 1.0) + delta)

    # Boost tags from user's declared interests
    user = db.session.get(User, user_id)
    if user and user.interests:
        for tag in [t.strip() for t in user.interests.split(",") if t.strip()]:
            tag_weights[tag] = tag_weights.get(tag, 1.0) + 2.0

    def score(article):
        tags = article.tag_list()
        if not tags:
            return 1.0
        return sum(tag_weights.get(t, 1.0) for t in tags) / len(tags)

    return max(candidates, key=score)


def _check_nudge():
    """After every 3 article interactions (react or skip), nudge if tasks are due today/this week."""
    today_str = date.today().isoformat()
    week_end_str = (date.today() + timedelta(days=7)).isoformat()
    if session.get("interact_date") != today_str:
        session["interact_date"] = today_str
        session["interact_count"] = 0

    session["interact_count"] = session.get("interact_count", 0) + 1
    session.modified = True

    if session["interact_count"] >= 3:
        session["interact_count"] = 0
        has_due = Task.query.filter(
            Task.user_id == current_user.id,
            Task.status != "completed",
            Task.due_date.isnot(None),
            Task.due_date <= week_end_str,
        ).first()
        if has_due:
            session["show_work_modal"] = True
        session.modified = True


@bp.post("/articles/<int:aid>/react")
@login_required
def react(aid: int):
    reaction = request.form.get("reaction", "").strip()
    if reaction not in ("liked", "disliked"):
        flash("Invalid reaction.", "danger")
        return redirect(url_for("main.index"))

    article = Article.query.get(aid)
    if not article:
        flash("Article not found.", "danger")
        return redirect(url_for("main.index"))

    existing = ArticleReaction.query.filter_by(
        user_id=current_user.id, article_id=aid
    ).first()
    if existing:
        existing.reaction = reaction
    else:
        db.session.add(ArticleReaction(
            user_id=current_user.id, article_id=aid, reaction=reaction
        ))
    db.session.commit()

    if reaction == "liked":
        flash("Saved to your reading log.", "success")

    _check_nudge()

    redirect_to = request.form.get("redirect_to", "").strip()
    if redirect_to and redirect_to.startswith("/") and not redirect_to.startswith("//"):
        return redirect(redirect_to)
    return redirect(url_for("main.index"))


@bp.post("/articles/<int:aid>/skip")
@login_required
def skip(aid: int):
    today = date.today().isoformat()
    if session.get("skip_date") != today:
        session["skip_date"] = today
        session["skipped_ids"] = []

    skipped = list(session.get("skipped_ids", []))
    if aid not in skipped:
        skipped.append(aid)
    session["skipped_ids"] = skipped
    session.modified = True

    _check_nudge()

    return redirect(url_for("main.index"))


ARTICLE_CATEGORIES = [
    "General", "Medicine", "Leadership", "Psychology",
    "Strategy", "Research", "MBA", "Personal Development",
]

@bp.get("/articles")
@login_required
def browse_articles():
    """All articles the user hasn't dismissed, with save/dismiss actions."""
    q = request.args.get("q", "").strip()
    cat = request.args.get("category", "").strip()

    reacted_ids = {
        r.article_id
        for r in ArticleReaction.query.filter_by(user_id=current_user.id).all()
    }
    saved_ids = {
        r.article_id
        for r in ArticleReaction.query.filter_by(
            user_id=current_user.id, reaction="liked"
        ).all()
    }

    # Show only user's own articles
    query = Article.query.filter(Article.added_by == current_user.id)
    if q:
        like = f"%{q}%"
        query = query.filter(
            db.or_(Article.title.ilike(like), Article.author.ilike(like), Article.tags.ilike(like))
        )
    if cat:
        query = query.filter(Article.category == cat)
    all_articles = query.order_by(Article.category.asc(), Article.title.asc()).all()

    from collections import defaultdict
    grouped = defaultdict(list)
    for a in all_articles:
        if a.content_type == "Note":
            grouped["\U0001f4dd Notes"].append(a)
        elif a.id in saved_ids:
            grouped["\u2713 Read"].append(a)
        else:
            grouped[a.category or "Uncategorized"].append(a)
    # Notes first, then alphabetical categories, then Read at end
    special = ["\U0001f4dd Notes", "\u2713 Read"]
    sorted_cats = (["\U0001f4dd Notes"] if "\U0001f4dd Notes" in grouped else []) + \
                  sorted([k for k in grouped if k not in special]) + \
                  (["\u2713 Read"] if "\u2713 Read" in grouped else [])
    grouped_articles = [(c, grouped[c]) for c in sorted_cats]

    return render_template(
        "articles_browse.html",
        grouped_articles=grouped_articles,
        all_articles=all_articles,
        saved_ids=saved_ids,
        reacted_ids=reacted_ids,
        q=q,
        cat=cat,
        categories=ARTICLE_CATEGORIES,
    )


@bp.get("/articles/add")
@login_required
def new_article():
    return render_template("articles_add.html", categories=ARTICLE_CATEGORIES)


@bp.post("/articles/create-note-json")
@login_required
def create_note():
    title = request.form.get("title", "").strip()
    body  = request.form.get("body", "").strip()
    tags_list = request.form.getlist("tags")
    tags = ", ".join(t.strip() for t in tags_list if t.strip())
    if not title:
        return jsonify(ok=False, error="Title is required.")
    if not body:
        return jsonify(ok=False, error="Note body is required.")
    a = Article(
        title=title,
        summary=body,
        url="",
        content_type="Note",
        tags=tags,
        added_by=current_user.id,
    )
    db.session.add(a)
    db.session.commit()
    return jsonify(ok=True)


@bp.post("/articles/add")
@login_required
def create_article():
    import os
    from werkzeug.utils import secure_filename
    from flask import current_app

    title   = request.form.get("title", "").strip()
    summary = request.form.get("summary", "").strip()
    url     = request.form.get("url", "").strip()
    author  = request.form.get("author", "").strip()
    tags_list = request.form.getlist("tags")
    tags    = ", ".join(t.strip() for t in tags_list if t.strip())
    category = request.form.get("category", "").strip()

    pdf_file = request.files.get("pdf")
    pdf_path = None
    if pdf_file and pdf_file.filename:
        if os.getenv("FLASK_ENV") == "production":
            flash("File uploads are not available in the hosted version — please use a URL instead.", "warning")
            return redirect(url_for("articles.new_article"))
        fname = secure_filename(pdf_file.filename)
        ext = fname.rsplit('.', 1)[-1].lower() if '.' in fname else ''
        if ext not in ('pdf', 'doc', 'docx'):
            flash("Only PDF, DOC, or DOCX files are allowed.", "danger")
            return redirect(url_for("articles.new_article"))
        upload_dir = os.path.join(current_app.static_folder, "uploads")
        os.makedirs(upload_dir, exist_ok=True)
        # prefix with user_id to avoid collisions
        saved = f"{current_user.id}_{fname}"
        pdf_file.save(os.path.join(upload_dir, saved))
        pdf_path = f"uploads/{saved}"

    if not title or not summary:
        flash("Title is required.", "danger")
        return redirect(url_for("articles.new_article"))
    if not url and not pdf_path:
        flash("Provide a URL or upload a PDF.", "danger")
        return redirect(url_for("articles.new_article"))

    db.session.add(Article(
        title=title, summary=summary, url=url or "",
        author=author or None, tags=tags,
        category=category or None,
        pdf_path=pdf_path,
        added_by=current_user.id
    ))
    db.session.commit()
    flash("Article added.", "success")
    return redirect(url_for("articles.browse_articles"))


@bp.post("/articles/<int:aid>/notes-json")
@login_required
def save_notes(aid: int):
    a = Article.query.filter_by(id=aid, added_by=current_user.id).first()
    if not a:
        return jsonify(ok=False, error="Not found.")
    a.notes = request.form.get("notes", "").strip() or None
    db.session.commit()
    return jsonify(ok=True)


@bp.post("/articles/<int:aid>/mark-read")
@login_required
def mark_read(aid: int):
    from datetime import datetime
    r = ArticleReaction.query.filter_by(
        user_id=current_user.id, article_id=aid, reaction="liked"
    ).first()
    if r:
        r.read_at = datetime.utcnow()
        db.session.commit()
    return redirect(url_for("articles.reading_log"))


@bp.post("/articles/<int:aid>/delete")
@login_required
def delete_article(aid: int):
    a = Article.query.filter_by(id=aid, added_by=current_user.id).first()
    if a:
        ArticleReaction.query.filter_by(article_id=aid).delete()
        db.session.delete(a)
        db.session.commit()
    return redirect(url_for("articles.browse_articles"))


@bp.post("/articles/<int:aid>/unmark-read")
@login_required
def unmark_read(aid: int):
    r = ArticleReaction.query.filter_by(
        user_id=current_user.id, article_id=aid, reaction="liked"
    ).first()
    if r:
        r.read_at = None
        db.session.commit()
    return redirect(url_for("articles.reading_log"))


@bp.get("/reading")
@login_required
def reading_log():
    liked = (
        ArticleReaction.query
        .filter_by(user_id=current_user.id, reaction="liked")
        .order_by(ArticleReaction.created_at.desc())
        .all()
    )
    to_read = []
    already_read = []
    for r in liked:
        a = db.session.get(Article, r.article_id)
        if a:
            if r.read_at:
                already_read.append((a, r.created_at, r.read_at))
            else:
                to_read.append((a, r.created_at))
    return render_template("reading_log.html",
                           to_read=to_read, already_read=already_read,
                           categories=ARTICLE_CATEGORIES)
