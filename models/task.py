from datetime import datetime                           # timestamp helper
from zoneinfo import ZoneInfo                           # stdlib time zones (Py 3.9+)
EASTERN = ZoneInfo("America/New_York")                  # US/Eastern tz
from . import db                                  # shared SQLAlchemy db object                   # import db

ALLOWED_STATUSES = ("pending", "in_progress", "completed")  # valid task states                   # enum-like tuple

class Task(db.Model):                              # SQLAlchemy model → table “tasks”             # define Task model
    __tablename__ = "tasks"                        # explicit table name                           # set table name

    id = db.Column(db.Integer, primary_key=True)   # unique row id                                 # primary key
    user_id = db.Column(db.Integer, nullable=False)        # owner user id (scopes data per user)  # user ownership
    patient_id = db.Column(db.Integer, nullable=False)     # the patient this task belongs to       # link to patient
    description = db.Column(db.Text, nullable=False)       # what needs to be done                  # task text
    due_date = db.Column(db.String(10), nullable=True)     # optional due date "YYYY-MM-DD"         # due date (string)
    status = db.Column(db.String(20), nullable=False, default="pending")  # task status             # status with default
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(EASTERN).replace(tzinfo=None))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(EASTERN).replace(tzinfo=None),
        onupdate=lambda: datetime.now(EASTERN).replace(tzinfo=None),
    )


    __table_args__ = (                             # extra DB hints                                 # table options
        db.Index("ix_tasks_user_due", "user_id", "due_date"),        # speed list queries by user/due   # index
        db.Index("ix_tasks_patient", "patient_id"),                  # speed queries by patient         # index
    )

    def __repr__(self):                            # debug-friendly repr                             # repr
        return f"<Task {self.id} status={self.status}>"
