from datetime import datetime
from zoneinfo import ZoneInfo
EASTERN = ZoneInfo("America/New_York")
from . import db

LIST_COLORS = ["#3498db","#e74c3c","#2ecc71","#9b59b6","#f39c12","#1abc9c","#e67e22","#e84393"]

class TaskList(db.Model):
    __tablename__ = "lists"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(EASTERN).replace(tzinfo=None))

    __table_args__ = (
        db.Index("ix_lists_user_name", "user_id", "name"),
    )

    @property
    def color(self):
        return LIST_COLORS[(self.id - 1) % len(LIST_COLORS)]

    def display_label(self) -> str:
        return self.name

    def __repr__(self):
        return f"<TaskList {self.id} {self.name!r}>"
