from datetime import datetime
from zoneinfo import ZoneInfo
EASTERN = ZoneInfo("America/New_York")
from . import db


class Article(db.Model):
    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(500), nullable=False, default="")
    author = db.Column(db.String(100), nullable=True)
    tags = db.Column(db.String(300), nullable=False, default="")
    category = db.Column(db.String(100), nullable=True)
    pdf_path = db.Column(db.String(300), nullable=True)
    added_by = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(EASTERN).replace(tzinfo=None))

    __table_args__ = (
        db.Index("ix_articles_added_by", "added_by"),
    )

    def tag_list(self):
        return [t.strip() for t in self.tags.split(",") if t.strip()]

    def __repr__(self):
        return f"<Article {self.id} {self.title!r}>"


class ArticleReaction(db.Model):
    __tablename__ = "article_reactions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    article_id = db.Column(db.Integer, nullable=False)
    reaction = db.Column(db.String(10), nullable=False)  # 'liked' or 'disliked'
    read_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(EASTERN).replace(tzinfo=None))

    __table_args__ = (
        db.UniqueConstraint("user_id", "article_id", name="uq_reaction_user_article"),
        db.Index("ix_reactions_user", "user_id"),
        db.Index("ix_reactions_article", "article_id"),
    )

    def __repr__(self):
        return f"<ArticleReaction user={self.user_id} article={self.article_id} {self.reaction}>"
