# CLINICAL TASK MANAGER
#### Video Demo:  <URL HERE>
#### Description:

# Clinical Task Manager
The care of patients with complex medical conditions generates a relentless stream of discrete, time-sensitive tasks. Each new consultation triggers a cascade: imaging to be ordered, pathology slides to be reviewed, tumor boards to be scheduled, insurance authorizations to be secured, surgical clearances to be obtained, follow-up visits to be coordinated. Multiply that workflow by hundreds of patients each year and the risk becomes obvious: critical steps can be delayed or lost entirely in the shuffle of phone calls, sticky notes, and fragmented EHR task lists.

This Clinical Task Manager is designed to solve this problem. It centralizes all patient-related tasks into a single, lightweight intuitive interface that is both flexible and disciplined. Each patient has a unique profile, and every required task can be assigned, tracked, and annotated over the full span of their care. Tasks carry due dates, statuses, and comments, making accountability transparent. Features like color-coded status indicators, due-date validation, and linked patient records reduce the cognitive burden on clinicians and staff, ensuring nothing slips through unnoticed.

The philosophy behind this application is simplicity in service of reliability. It avoids unnecessary complexity while focusing on the essentials: capture the task, tie it to the patient, track it to completion. By creating an architecture that balances usability with structure, the Clinical Task Manager functions like a safety net woven directly into the clinical workflow. In doing so, it protects patients from delays, lightens administrative load, and gives clinical teams confidence that every detail of complex care is being handled.

As the Clinical Task Manager matures, potential enhancements include adding role-based permissions so different team members (surgeons, nurses, coordinators) can interact with patient tasks at the appropriate level, integrating automated reminders via email or text, and eventually linking with the electronic health record to reduce duplicate data entry. The main challenge ahead lies in security and HIPAA compliance: currently this app is a prototype for workflow organization, but storing protected health information (PHI) would require strict safeguards such as encryption at rest and in transit, audit logging, secure authentication, access control, and compliance with institutional IT policies. Scaling from a personal productivity tool into a HIPAA-compliant clinical system is feasible but involves regulatory, technical, and administrative layers that extend beyond coding.


## Features include:
- User registration and login (Flask-Login, Flask-Bcrypt)
- Patient management (add, list, delete with safeguards)
- Task management (add, edit, delete, comments, due dates)
- Validations: block past due dates, block deleting patients with tasks
- Simple Bootstrap UI


## Distinctiveness and Complexity
- Goes beyond a to-do list by linking tasks to patients, which introduces relational database logic.
- Implements user authentication with password hashing.
- Includes custom validations (no past due dates, block patient deletion if tasks exist).
- Multiple models (User, Patient, Task, Comment) with relationships.
- Frontend enhancements: calendar date picker, status color coding, confirmation prompts.


## Files

### **Core application structure**

* **`app.py`**

  * Creates and configures the Flask application.
  * Initializes database, login manager, and blueprints.
  * Central hub that ties everything together.

* **`__init__.py` (in root `patients/`)**

  * Initializes the SQLAlchemy `db` object so it can be shared by models.
  * Keeps package imports clean.

* **`requirements.txt`**
  * List of all Python dependencies 
  

### **Models (Database tables)**

Located in `patients/models/` — each represents a table in the database.

* **user.py** → `User` table
  * Stores account credentials (username, hashed password).
  * Required for authentication.

* **`patient.py`** → `Patient` table
  * Stores patient demographics and identifiers (MRN, name, DOB).
  * Each patient is linked to a `user` (the account that created them).

* **`task.py`** → `Task` table
  * Stores tasks tied to a patient (description, due date, status).
  * Validates that due dates are not in the past.
  * Linked to both `Patient` and `User`.

* **`comment.py`** → `Comment` table
  * Stores free-text comments attached to a task.
  * Includes timestamp (auto-generated, formatted as EST).
  * Linked to both `Task` and `User`.

---

### **Routes (Views & Controllers)**

Located in `patients/routes/`. Each file defines a Flask *Blueprint* (a modular set of routes).
* **`main.py`**

  * Home page, navigation bar.
  * Renders dashboard-like view.

* **`auth.py`**
  * Handles registration, login, and logout.
  * Uses Flask-Login to manage sessions.

* **`patients.py`**
  * Lists patients for the logged-in user.
  * Allows adding, editing, and deleting patients.
  * Blocks deletion if patient has active tasks.

* **`tasks.py`**
  * Lists tasks for a given patient.
  * Allows creating, editing, deleting tasks.
  * Handles comments linked to tasks.
  * Implements due date validation and status updates.

---

### **Templates (Frontend HTML)**

Located in `patients/templates/`.

* **`layout.html`**
  * Base template with Bootstrap, navigation bar, flash messages.
  * Other pages extend this layout.

* **`index.html`**
  * Main landing page after login.
  * Shows welcome/dashboard.

* **`patients_list.html`**
  * Displays all patients for the logged-in user.
  * Add/edit/delete patient buttons.

* **`tasks_list.html`**
  * Displays all tasks for a patient.
  * Color-coded statuses, due dates, comments.
  * Edit/delete task buttons.

* **`register.html`, `login.html`**
  * Authentication forms.

