# RConnect – College Club Management System

RConnect is a Django-based college club management platform for Rajagiri College of Social Sciences (RCSS). It lets students discover clubs, apply for auditions, register for events, receive notifications, and track activities. Club and Union administrators manage their own content, while Super Admin uses Django Admin for complete control.

## Technologies
- Python
- Django
- SQLite
- HTML5 / CSS3 / JavaScript
- Bootstrap 5
- Pillow

## Main features
- Student self-registration and secure authentication
- Custom User model with four roles: Student, Club Admin, Union Admin, Super Admin
- Four organizational clubs: Dance Club, Music Club, C-Star, Fashion Club
- Separate College Union model
- Club membership with duplicate protection
- Audition applications and approval workflow
- Automatic membership creation when an audition application is selected
- Events for clubs or the College Union
- Event registration and admin approval workflow
- Deadline and cancellation validation
- In-system notifications and unread/read state
- Announcements
- Club/student achievements
- Image uploads for profiles, clubs, events, gallery and achievements
- Django Admin for full system management
- Responsive green/white academic UI
- Clean empty states; no fake demo content

## Important data policy
The database starts without fake students, events, auditions, registrations, announcements, achievements, gallery photos, or competitions. The migrations create only the four required clubs and one College Union. Real content should be entered through the application or Django Admin.

No plaintext passwords are included anywhere.

## Installation – Windows

Open Command Prompt or PowerShell and go into the extracted project folder:

```powershell
cd RConnect
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py check
python manage.py migrate
```

Create the Super Admin securely:

```powershell
python manage.py createsuperuser
```

The command will ask you for the username/email and password. The password is not stored in this README.

### Optional: create the specified Club/Union Admin accounts securely

Run:

```powershell
python manage.py setup_admins
```

The command creates/updates:
- Aarathi Shankar — aarathi@gmail.com — Club Admin — Dance Club
- Abina Jaleel — Abina@gmail.com — Club Admin — Music Club
- Jesna Jacob — Jesna@gmail.com — Club Admin — C-Star
- Dilna Biju — Dilna@gmail.com — Club Admin — Fashion Club
- Haleema Fahma M C — haleema@gmail.com — Union Admin — College Union

For each account, the terminal prompts for a password. Passwords are hashed using Django and are never written to source files.

Run the server:

```powershell
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

Django Admin:

```text
http://127.0.0.1:8000/admin/
```

## First-use order
1. Create the Super Admin.
2. Run `python manage.py setup_admins` if you want the five specified admin accounts.
3. Log in as a Club Admin or Union Admin and add real content.
4. Register a student from the RConnect Register page.
5. Use the student account to apply for real auditions and register for real events.
6. Use the relevant administrator account to approve/reject applications and registrations.
7. Verify that notifications appear for both sides of the workflow.

## Project structure

```text
RConnect/
├── manage.py
├── rconnect/
├── accounts/
├── clubs/
├── events/
├── auditions/
├── core/
├── templates/
├── static/
├── media/
├── requirements.txt
└── README.md
```

## Security notes
- Django CSRF protection is enabled.
- Passwords use Django's password hashing.
- Role checks are enforced server-side.
- Club Admin views are filtered to the assigned club.
- Union Admin views are filtered to the College Union.
- Students can only access their own applications, registrations and notifications.
- Database uniqueness constraints prevent duplicate memberships, audition applications and event registrations.
- Development media is served by Django. For production, configure a proper web server and production security settings.
