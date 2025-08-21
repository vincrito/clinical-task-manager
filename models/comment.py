from datetime import datetime                 # timestamps for created_at                         # import datetime
from . import db                              # shared SQLAlchemy db object                        # import db
from zoneinfo import ZoneInfo                           # stdlib time zones (Py 3.9+)
EASTERN = ZoneInfo("America/New_York")                  # US/Eastern tz

class Comment(db.Model):                      # SQLAlchemy model → table “comments”               # define Comment
    __tablename__ = "comments"                # explicit table name                                # set table name

    id = db.Column(db.Integer, primary_key=True)                 # unique row id                  # primary key
    task_id = db.Column(db.Integer, nullable=False)              # which task this comment is on  # link to task
    user_id = db.Column(db.Integer, nullable=False)              # who wrote it (owner user id)   # author id
    body = db.Column(db.Text, nullable=False)                    # the comment text               # content
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(EASTERN).replace(tzinfo=None))



    __table_args__ = (                               # extra DB hints                               # table opts
        db.Index("ix_comments_task", "task_id"),     # speed lookups by task                        # index
        db.Index("ix_comments_user", "user_id"),     # speed lookups by user                        # index
    )

    def __repr__(self):                               # debug string                                # repr
        return f"<Comment {self.id} on task {self.task_id}>"
