from flask import Blueprint, render_template, request, redirect, url_for, flash  # page rendering, forms, redirects, alerts  # imports
from flask_login import login_required, current_user                              # require login and access current user     # imports
from models import db                                                             # db session for commits                    # imports
from models.patient import Patient                                                 # Patient model                            # imports
from models.task import Task

bp = Blueprint("patients", __name__)                                              # blueprint named "patients"                # blueprint

@bp.get("/patients")                                                              # list page for patients (GET)              # route
@login_required                                                                    # must be logged in                         # guard
def list_patients():
    q = request.args.get("q", "").strip()                                         # optional search query from ?q=            # read query
    base = Patient.query.filter_by(user_id=current_user.id)                       # only this user's patients                 # scope by user
    if q:                                                                         # if a search term was provided             # condition
        like = f"%{q}%"                                                           # SQL LIKE pattern                          # pattern
        base = base.filter(                                                       # add filters for name or MRN               # filter
            db.or_(Patient.last_name.ilike(like),
                   Patient.first_name.ilike(like),
                   Patient.mrn.ilike(like))
        )
    rows = base.order_by(Patient.last_name.asc(), Patient.first_name.asc()).all() # sorted results                            # query
    return render_template("patients_list.html", patients=rows, q=q)              # render list template                      # render

@bp.get("/patients/new")                                                          # new patient form (GET)                     # route
@login_required                                                                    # must be logged in                          # guard
def new_patient():
    return render_template("patients_new.html")                                    # render creation form                       # render

@bp.post("/patients/new")                                                         # handle create (POST)                        # route
@login_required                                                                    # must be logged in                           # guard
def create_patient():
    last = request.form.get("last_name", "").strip()                               # read last name                              # form
    first = request.form.get("first_name", "").strip()                              # read first name                             # form
    mrn = request.form.get("mrn", "").strip()                                       # read MRN (optional)                         # form
    dob = request.form.get("dob", "").strip()                                       # read DOB (optional)                         # form

    if not (last or mrn):                                                           # require at least last name OR MRN           # validate
        flash("Provide at least last name or MRN.", "danger")                       # show error                                  # alert
        return redirect(url_for("patients.new_patient"))                            # back to form                                # redirect

    p = Patient(user_id=current_user.id, last_name=last or None,                    # build Patient row                           # create
                first_name=first or None, mrn=mrn or None, dob=dob or None)         # set optional fields                         # fields
    db.session.add(p)                                                                # stage insert                                # db
    db.session.commit()                                                              # commit to database                          # db
    flash("Patient created.", "success")                                             # success message                             # alert
    return redirect(url_for("patients.list_patients"))                               # go to list                                  # redirect

@bp.get("/patients/<int:pid>")                                                     # route: GET /patients/<pid> shows detail page                     # route
@login_required                                                                     # ensure user is logged in                                         # guard
def patient_detail(pid: int):
    p = Patient.query.filter_by(id=pid, user_id=current_user.id).first_or_404()     # fetch patient owned by current user or 404                      # query
    from models.task import Task                                                    # import here to avoid circular import issues                      # import
    tasks = (Task.query                                                             # build a query for this patient's tasks                           # query
             .filter_by(user_id=current_user.id, patient_id=p.id)                   # only tasks owned by me and linked to this patient                # scope
             .order_by(Task.due_date.asc().nulls_last(), Task.created_at.desc())   # sort: earliest due, then newest created                          # order
             .all())                                                                # execute query                                                     # exec
    return render_template("patient_detail.html", patient=p, tasks=tasks)           # render template with patient + their tasks                       # render

@bp.get("/patients/<int:pid>/edit")                                               # serve the edit form for a patient
@login_required                                                                    # only logged-in users
def edit_patient(pid: int):
    p = Patient.query.filter_by(id=pid, user_id=current_user.id).first_or_404()    # fetch patient you own or 404
    return render_template("patients_edit.html", patient=p)                        # render edit template with current values

@bp.post("/patients/<int:pid>/edit")                                              # process the edit form submission
@login_required                                                                    # only logged-in users
def update_patient(pid: int):
    p = Patient.query.filter_by(id=pid, user_id=current_user.id).first_or_404()    # fetch patient you own or 404

    last = request.form.get("last_name", "").strip()                               # read updated last name
    first = request.form.get("first_name", "").strip()                             # read updated first name
    mrn = request.form.get("mrn", "").strip()                                      # read updated MRN (optional)
    dob = request.form.get("dob", "").strip()                                      # read updated DOB (optional)

    if not (last or mrn):                                                          # require at least last name or MRN
        flash("Provide at least last name or MRN.", "danger")                      # error message
        return redirect(url_for("patients.edit_patient", pid=pid))                 # back to edit form

    p.last_name = last or None                                                     # assign (None if blank)
    p.first_name = first or None                                                   # assign (None if blank)
    p.mrn = mrn or None                                                            # assign (None if blank)
    p.dob = dob or None                                                            # assign (None if blank)

    db.session.commit()                                                            # save changes
    flash("Patient updated.", "success")                                           # success message
    return redirect(url_for("patients.patient_detail", pid=pid))                   # go back to patient detail

@bp.post("/patients/<int:pid>/delete")                                            # delete a patient (and, by design, keep tasks)
@login_required                                                                    # only logged-in users
def delete_patient(pid: int):
    p = Patient.query.filter_by(id=pid, user_id=current_user.id).first()           # fetch patient you own
    if not p:                                                                      # if not found
        flash("Patient not found.", "danger")                                      # error message
        return redirect(url_for("patients.list_patients"))                         # back to list
    # NOTE: We are NOT cascading delete to tasks here to avoid accidental data loss.
    # If you want to block deletion when tasks exist, add a guard:
    # from models.task import Task
    # if Task.query.filter_by(patient_id=p.id, user_id=current_user.id).first():
    #     flash("Cannot delete: patient has tasks.", "danger")
    #     return redirect(url_for("patients.patient_detail", pid=pid))

        # block deletion if any tasks exist for this patient (owned by current user)             # comment
    has_tasks = Task.query.filter_by(user_id=current_user.id, patient_id=p.id).first()       # query
    if has_tasks:                                                                            # any row found?
        flash("Cannot delete: patient has tasks. Delete or reassign tasks first.", "danger") # message
        return redirect(url_for("patients.patient_detail", pid=pid))                         # back

    db.session.delete(p)                                                           # stage deletion
    db.session.commit()                                                            # apply deletion
    flash("Patient deleted.", "success")                                           # success message
    return redirect(url_for("patients.list_patients"))                             # back to list
