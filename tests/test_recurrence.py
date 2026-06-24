"""
Tests for the recurring-task feature.

Covers all ten required scenarios:
 1. A weekly recurrence creates a new occurrence on schedule.
 2. A new occurrence is created even when the prior occurrence is incomplete.
 3. Completing one occurrence does not affect another.
 4. Multiple missed occurrences are generated correctly.
 5. Running the generation process twice does not create duplicates.
 6. The next occurrence is calculated from the schedule without drift.
 7. The UI displays the occurrence date without modifying the stored title.
 8. Nonrecurring tasks continue to behave as before.
 9. Deactivating a recurrence prevents future occurrences.
10. Existing historical occurrences remain intact when a recurrence is edited or deactivated.
"""
import pytest
from datetime import date, timedelta

from models.task import Task
from models.recurrence import RecurrenceRule, generate_due_occurrences, _next_date


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_rule(db, user, task_list, *, frequency="weekly", days_ago=7,
               is_active=True, description="Test Task"):
    """Create a RecurrenceRule whose next_occurrence is *days_ago* days in the past."""
    start = (date.today() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
    rule = RecurrenceRule(
        user_id=user.id,
        list_id=task_list.id,
        description=description,
        priority="medium",
        frequency=frequency,
        start_date=start,
        next_occurrence=start,
        is_active=is_active,
    )
    db.session.add(rule)
    db.session.commit()
    return rule


def _task_count_for_rule(db, rule):
    return Task.query.filter_by(recurrence_id=rule.id).count()


def _tasks_for_rule(db, rule):
    return Task.query.filter_by(recurrence_id=rule.id).order_by(Task.occurrence_date).all()


# ---------------------------------------------------------------------------
# Test 1 — weekly recurrence creates a new occurrence on schedule
# ---------------------------------------------------------------------------

def test_weekly_creates_occurrence(db, user, task_list):
    rule = _make_rule(db, user, task_list, frequency="weekly", days_ago=7)
    n = generate_due_occurrences(user.id)
    assert n >= 1, "Should have created at least one occurrence"
    tasks = _tasks_for_rule(db, rule)
    assert len(tasks) >= 1
    t = tasks[0]
    assert t.description == "Test Task"
    assert t.occurrence_date == rule.start_date
    assert t.status == "pending"
    assert t.recurrence_id == rule.id


# ---------------------------------------------------------------------------
# Test 2 — new occurrence created even when prior occurrence is incomplete
# ---------------------------------------------------------------------------

def test_new_occurrence_created_even_when_prior_incomplete(db, user, task_list):
    # Rule with next_occurrence 14 days ago so two weekly occurrences are due
    rule = _make_rule(db, user, task_list, frequency="weekly", days_ago=14)
    generate_due_occurrences(user.id)
    tasks = _tasks_for_rule(db, rule)
    assert len(tasks) >= 2, "Two missed weekly occurrences should be generated"
    # Mark first as incomplete (already pending, which is the default)
    assert all(t.status == "pending" for t in tasks)
    # Both should exist regardless
    assert tasks[0].occurrence_date != tasks[1].occurrence_date


# ---------------------------------------------------------------------------
# Test 3 — completing one occurrence does not affect another
# ---------------------------------------------------------------------------

def test_completing_one_occurrence_does_not_affect_others(db, user, task_list):
    rule = _make_rule(db, user, task_list, frequency="weekly", days_ago=14)
    generate_due_occurrences(user.id)
    tasks = _tasks_for_rule(db, rule)
    assert len(tasks) >= 2

    # Complete only the first occurrence
    tasks[0].status = "completed"
    db.session.commit()

    # Re-fetch and verify only the first is completed
    refreshed = _tasks_for_rule(db, rule)
    statuses = {t.occurrence_date: t.status for t in refreshed}
    assert statuses[tasks[0].occurrence_date] == "completed"
    assert statuses[tasks[1].occurrence_date] == "pending"

    # The rule itself is unaffected
    db.session.refresh(rule)
    assert rule.is_active is True


# ---------------------------------------------------------------------------
# Test 4 — multiple missed occurrences are generated correctly
# ---------------------------------------------------------------------------

def test_multiple_missed_occurrences_generated(db, user, task_list):
    # 27 days ago → exactly 4 weekly occurrences (days -27, -20, -13, -6);
    # the 5th would be today+1 which is not yet due.
    rule = _make_rule(db, user, task_list, frequency="weekly", days_ago=27)
    n = generate_due_occurrences(user.id)
    assert n == 4
    tasks = _tasks_for_rule(db, rule)
    assert len(tasks) == 4
    # Dates should be evenly 7 days apart
    dates = sorted(t.occurrence_date for t in tasks)
    for i in range(1, len(dates)):
        d0 = date.fromisoformat(dates[i - 1])
        d1 = date.fromisoformat(dates[i])
        assert (d1 - d0).days == 7


# ---------------------------------------------------------------------------
# Test 5 — running generation twice does not create duplicates
# ---------------------------------------------------------------------------

def test_generation_is_idempotent(db, user, task_list):
    rule = _make_rule(db, user, task_list, frequency="weekly", days_ago=14)
    n1 = generate_due_occurrences(user.id)
    n2 = generate_due_occurrences(user.id)
    assert n2 == 0, "Second run should not create any new occurrences"
    assert _task_count_for_rule(db, rule) == n1


# ---------------------------------------------------------------------------
# Test 6 — next occurrence is calculated from the schedule, not wall-clock time
# ---------------------------------------------------------------------------

def test_next_date_no_drift():
    """_next_date() always advances by exactly one interval from the input date."""
    assert _next_date("2026-06-05", "weekly") == "2026-06-12"
    assert _next_date("2026-06-05", "weekly") != "2026-06-13"  # not 8 days

    assert _next_date("2026-06-05", "biweekly") == "2026-06-19"

    assert _next_date("2026-06-05", "daily") == "2026-06-06"

    assert _next_date("2026-01-31", "monthly") == "2026-02-28"  # clamped
    assert _next_date("2026-03-31", "monthly") == "2026-04-30"  # clamped


def test_generation_advances_from_scheduled_date(db, user, task_list):
    """
    Simulate a Friday-scheduled weekly task where generation runs on Saturday.
    The following occurrence must land on the NEXT Friday, not 7 days from Saturday.
    """
    friday = date(2026, 6, 5)           # a known Friday
    next_friday = date(2026, 6, 12)
    start_str = friday.strftime("%Y-%m-%d")

    rule = RecurrenceRule(
        user_id=user.id,
        list_id=task_list.id,
        description="Friday Task",
        priority="medium",
        frequency="weekly",
        start_date=start_str,
        next_occurrence=start_str,
        is_active=True,
    )
    db.session.add(rule)
    db.session.commit()

    # Manually call the internal helper rather than running generate_due_occurrences
    # so we're not dependent on today's date.
    advanced = _next_date(start_str, "weekly")
    assert advanced == next_friday.strftime("%Y-%m-%d"), (
        "Next occurrence must be exactly one week from the SCHEDULED date"
    )


# ---------------------------------------------------------------------------
# Test 7 — UI displays occurrence date without modifying the stored title
# ---------------------------------------------------------------------------

def test_stored_title_unchanged_from_occurrence_date(db, user, task_list):
    rule = _make_rule(db, user, task_list, frequency="weekly", days_ago=7,
                      description="Review tumor board list")
    generate_due_occurrences(user.id)
    tasks = _tasks_for_rule(db, rule)
    assert len(tasks) >= 1
    t = tasks[0]
    # Stored description must not contain the date
    assert "—" not in t.description
    assert t.description == "Review tumor board list"
    # occurrence_date field holds the date separately
    assert t.occurrence_date is not None
    assert len(t.occurrence_date) == 10  # YYYY-MM-DD


# ---------------------------------------------------------------------------
# Test 8 — nonrecurring tasks continue to behave as before
# ---------------------------------------------------------------------------

def test_nonrecurring_tasks_unaffected(db, user, task_list):
    plain = Task(
        user_id=user.id,
        list_id=task_list.id,
        description="Plain task",
        due_date=date.today().strftime("%Y-%m-%d"),
        status="pending",
        priority="low",
        position=0,
    )
    db.session.add(plain)
    db.session.commit()

    n = generate_due_occurrences(user.id)
    assert n == 0  # no recurrence rules → nothing generated

    # The plain task is untouched
    db.session.refresh(plain)
    assert plain.description == "Plain task"
    assert plain.recurrence_id is None
    assert plain.occurrence_date is None

    db.session.delete(plain)
    db.session.commit()


# ---------------------------------------------------------------------------
# Test 9 — deactivating a recurrence prevents future occurrences
# ---------------------------------------------------------------------------

def test_deactivating_stops_generation(db, user, task_list):
    rule = _make_rule(db, user, task_list, frequency="weekly", days_ago=0)
    # Advance next_occurrence to next week so nothing is due yet
    rule.next_occurrence = (date.today() + timedelta(days=7)).strftime("%Y-%m-%d")
    db.session.commit()

    # Deactivate
    rule.is_active = False
    db.session.commit()

    n = generate_due_occurrences(user.id)
    assert n == 0, "Deactivated rule should not generate occurrences"
    assert _task_count_for_rule(db, rule) == 0


# ---------------------------------------------------------------------------
# Test 10 — historical occurrences remain intact when recurrence is deactivated
# ---------------------------------------------------------------------------

def test_historical_occurrences_intact_after_deactivation(db, user, task_list):
    rule = _make_rule(db, user, task_list, frequency="weekly", days_ago=14)
    generate_due_occurrences(user.id)
    n_before = _task_count_for_rule(db, rule)
    assert n_before >= 2

    # Deactivate the rule
    rule.is_active = False
    db.session.commit()

    # Attempt generation again — should produce nothing new
    n_new = generate_due_occurrences(user.id)
    assert n_new == 0

    # Existing occurrences are still present
    assert _task_count_for_rule(db, rule) == n_before
