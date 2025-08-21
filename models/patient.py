from datetime import datetime                           # timestamp helper
from zoneinfo import ZoneInfo                           # stdlib time zones (Py 3.9+)
EASTERN = ZoneInfo("America/New_York")                  # US/Eastern tz
from . import db                                   # shared SQLAlchemy db object            # import db

class Patient(db.Model):                            # SQLAlchemy model → table “patients”   # define Patient model
    __tablename__ = "patients"                      # explicit table name                    # set table name

    id = db.Column(db.Integer, primary_key=True)    # unique row id (auto-increment)         # primary key
    user_id = db.Column(db.Integer, nullable=False) # owner user id (single-tenant now)      # FK to users.id later (logic-enforced)
    mrn = db.Column(db.String(64), nullable=True)   # optional medical record number (mock)   # MRN (optional for demo)
    first_name = db.Column(db.String(80), nullable=True) # optional first name                # first name
    last_name = db.Column(db.String(80), nullable=True)  # optional last name                 # last name
    dob = db.Column(db.String(10), nullable=True)   # optional DOB "YYYY-MM-DD" (mock)        # date of birth (string for simplicity)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(EASTERN).replace(tzinfo=None))


    __table_args__ = (                              # extra DB hints                          # table options
        db.Index("ix_patients_user_last_first", "user_id", "last_name", "first_name"),  # search index  # composite index
    )

    def display_label(self) -> str:                 # helper for UI labels                    # display helper
        parts = [p for p in [self.last_name, self.first_name] if p]  # build "Last, First"   # collect name parts
        name = ", ".join(parts) if parts else f"Patient {self.id}"   # fallback to id        # name or fallback
        if self.mrn:                                # if MRN present                          # MRN exists?
            name += f" (MRN {self.mrn})"            # append MRN to label                     # add MRN
        return name                                  # return final label                      # return string

    def __repr__(self):                             # debug-friendly repr                      # repr
        return f"<Patient {self.id}>"
