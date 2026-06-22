from datetime import datetime                           # timestamp helper
from zoneinfo import ZoneInfo                           # stdlib time zones (Py 3.9+)
EASTERN = ZoneInfo("America/New_York")                  # US/Eastern tz
from . import db                                  # shared SQLAlchemy db object                   # import db

ALLOWED_STATUSES = ("pending", "in_progress", "completed")  # valid task states
ALLOWED_PRIORITIES = ("low", "medium", "high")              # valid priority levels

class Task(db.Model):                              # SQLAlchemy model → table “tasks”             # define Task model
    __tablename__ = "tasks"                        # explicit table name                           # set table name

    id = db.Column(db.Integer, primary_key=True)   # unique row id                                 # primary key
    user_id = db.Column(db.Integer, nullable=False)        # owner user id (scopes data per user)  # user ownership
    list_id = db.Column(db.Integer, nullable=False)         # the list this task belongs to
    description = db.Column(db.Text, nullable=False)       # what needs to be done                  # task text
    due_date = db.Column(db.String(10), nullable=True)     # optional due date "YYYY-MM-DD"         # due date (string)
    status = db.Column(db.String(20), nullable=False, default="pending")  # task status
    priority = db.Column(db.String(10), nullable=False, default="medium")  # low / medium / high
    position = db.Column(db.Integer, nullable=False, default=0)  # display order within list (lower = higher up)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(EASTERN).replace(tzinfo=None))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(EASTERN).replace(tzinfo=None),
        onupdate=lambda: datetime.now(EASTERN).replace(tzinfo=None),
    )


    __table_args__ = (                             # extra DB hints                                 # table options
        db.Index("ix_tasks_user_due", "user_id", "due_date"),
        db.Index("ix_tasks_list", "list_id"),
    )

    def __repr__(self):                            # debug-friendly repr                             # repr
        return f"<Task {self.id} status={self.status}>"
