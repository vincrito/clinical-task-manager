"""
RecurrenceRule model and occurrence-generation helpers.

A RecurrenceRule is the *template* for a repeating task. Each time an
occurrence becomes due, generate_due_occurrences() creates a regular Task
row, links it back to this rule via Task.recurrence_id, and advances
next_occurrence forward by one interval.

Frequencies supported: daily, weekly, biweekly, monthly.
Adding new intervals only requires extending _next_date() and the
ALLOWED_FREQUENCIES tuple — no schema changes needed.
"""

from calendar import monthrange
from datetime import datetime, timedelta, date as _date
from zoneinfo import ZoneInfo

from . import db

EASTERN = ZoneInfo("America/New_York")
ALLOWED_FREQUENCIES = ("daily", "weekly", "biweekly", "monthly")


class RecurrenceRule(db.Model):
    __tablename__ = "recurrence_rules"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    list_id = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(10), nullable=False, default="medium")
    frequency = db.Column(db.String(20), nullable=False)      # daily/weekly/biweekly/monthly
    start_date = db.Column(db.String(10), nullable=False)     # YYYY-MM-DD — first scheduled date
    next_occurrence = db.Column(db.String(10), nullable=False) # YYYY-MM-DD — next date to generate
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(EASTERN).replace(tzinfo=None),
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(EASTERN).replace(tzinfo=None),
        onupdate=lambda: datetime.now(EASTERN).replace(tzinfo=None),
    )

    __table_args__ = (
        db.Index("ix_recurrence_user", "user_id"),
    )

    def __repr__(self):
        return (
            f"<RecurrenceRule {self.id} freq={self.frequency!r}"
            f" next={self.next_occurrence!r} active={self.is_active}>"
        )


# ---------------------------------------------------------------------------
# Date arithmetic
# ---------------------------------------------------------------------------

def _next_date(date_str: str, frequency: str) -> str:
    """Return the next scheduled date string given a current date and frequency.

    Calculates from the *scheduled* date, not from the current wall-clock time,
    so schedule drift cannot accumulate even when generation runs late.
    """
    d = datetime.strptime(date_str, "%Y-%m-%d").date()
    if frequency == "daily":
        d += timedelta(days=1)
    elif frequency == "weekly":
        d += timedelta(weeks=1)
    elif frequency == "biweekly":
        d += timedelta(weeks=2)
    elif frequency == "monthly":
        # Advance by one calendar month; clamp to last day if needed (e.g. Jan 31 → Feb 28)
        year = d.year + (d.month // 12)
        month = (d.month % 12) + 1
        day = min(d.day, monthrange(year, month)[1])
        d = d.replace(year=year, month=month, day=day)
    else:
        # Unknown frequency: fall back to weekly so the loop does not hang
        d += timedelta(weeks=1)
    return d.strftime("%Y-%m-%d")


# ---------------------------------------------------------------------------
# Occurrence generation
# ---------------------------------------------------------------------------

def generate_due_occurrences(user_id: int) -> int:
    """Create all overdue recurring-task occurrences for *user_id*.

    Returns the number of new Task rows created.

    Design guarantees:
    - Idempotent: running twice produces the same result (unique constraint
      + existence check prevent duplicates).
    - Drift-free: next_occurrence advances from the *scheduled* date.
    - Catch-up: all occurrences from last run through today are generated in
      one call, so missed scheduler runs are recovered automatically.
    - Isolated: completing or deleting an occurrence never touches this rule
      or other occurrences.
    """
    from models.task import Task  # local import avoids circular dependency

    today_str = datetime.now(EASTERN).date().strftime("%Y-%m-%d")
    rules = RecurrenceRule.query.filter_by(user_id=user_id, is_active=True).all()

    created = 0
    had_work = False

    for rule in rules:
        while rule.next_occurrence <= today_str:
            had_work = True
            occ_date = rule.next_occurrence

            # Idempotency guard — skip if this occurrence already exists.
            # The DB-level unique index on (recurrence_id, occurrence_date)
            # provides a second safety net against races.
            existing = (
                Task.query
                .filter_by(recurrence_id=rule.id, occurrence_date=occ_date)
                .first()
            )
            if not existing:
                max_pos = (
                    db.session.query(db.func.max(Task.position))
                    .filter_by(user_id=user_id, list_id=rule.list_id)
                    .scalar()
                )
                next_pos = (max_pos + 1) if max_pos is not None else 0

                task = Task(
                    user_id=user_id,
                    list_id=rule.list_id,
                    description=rule.description,
                    due_date=occ_date,
                    status="pending",
                    priority=rule.priority,
                    position=next_pos,
                    recurrence_id=rule.id,
                    occurrence_date=occ_date,
                )
                db.session.add(task)
                created += 1

            # Always advance regardless of whether we just created the task —
            # prevents an infinite loop when the occurrence already existed.
            rule.next_occurrence = _next_date(occ_date, rule.frequency)

    if had_work:
        db.session.commit()

    return created
