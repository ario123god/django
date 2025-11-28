# Aurora School Website (Django)

A modern, responsive school management website built with Django, HTML, CSS, and vanilla JavaScript. Includes role-based dashboards for students, parents, teachers, and administrators plus CMS-style pages for admissions, academics, events, and communication.

## Features
- Custom user model with roles (student, parent, teacher, admin/owner) and authentication flows
- Online admissions, fee overview, scholarships, notices, FAQs, and contact form with Google Map embed
- Academics hub for subjects, syllabus items, timetable, study materials, assignments, and library catalogue
- Events, gallery, news/blog, newsletters, transport and hostel listings
- Dashboards tailored by role: students (assignments, materials, attendance, grades), parents (fees, notices), teachers (classes, assignments), admin (admission pipeline and analytics)
- Email-based password reset (console backend) and OTP verification placeholder
- Seed command to create demo users and content

## Quickstart
1. **Install dependencies** (Django 5+ is recommended). If network access is restricted, make sure Django is available locally.
   ```bash
   pip install django
   ```
2. **Apply migrations & create a superuser**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
3. **Load sample data** (optional demo users: admin/admin123, teacher1/teacher123, parent1/parent123, student1/student123)
   ```bash
   python manage.py seed_school
   ```
4. **Run the development server**
   ```bash
   python manage.py runserver
   ```
5. Visit `http://localhost:8000` to explore the site. Admin is available at `/admin/`.

## Project Structure
- `schoolsite/` – project settings and URL routing
- `core/` – app with models, views, forms, admin configuration, and demo seed command
- `templates/` – HTML templates for all pages, dashboards, and emails
- `static/` – CSS and JS with a light, modern theme

## Notes
- The email backend is configured to use Django's console backend for easy testing. Update `EMAIL_BACKEND` in `schoolsite/settings.py` for real delivery.
- Static assets use a minimal palette (white, light gray, light blue) with subtle hover effects and responsive layouts.
