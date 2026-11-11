# IT Skills Academy

A Django-based personal IT training lab with interactive lessons for programming,
IT support, hardware, and networking. Each learning path includes 20 beginner
lessons and 10 intermediate lessons, with quizzes and practice activities.

## Requirements

- Python 3.10 or newer
- pip

## Run locally (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_content
python manage.py runserver
```

Open <http://127.0.0.1:8000/> in your browser.

The local development settings use SQLite and a development-only secret key.
For deployment, set `DJANGO_SECRET_KEY` to a secure, unique value, set
`DJANGO_DEBUG=false`, and set `DJANGO_ALLOWED_HOSTS` to a comma-separated list
of the hostnames serving the application.

## Deploy on Render

Configure the Render web service with these commands:

- **Build Command:** `pip install -r requirements.txt && python manage.py migrate && python manage.py seed_content`
- **Start Command:** `gunicorn it_skills_academy.wsgi:application --bind 0.0.0.0:$PORT`

Set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=false`, and `DJANGO_ALLOWED_HOSTS` in the
service's environment variables. Include the service's `onrender.com` hostname
in `DJANGO_ALLOWED_HOSTS`. The WSGI application is
`it_skills_academy.wsgi:application`; `academy.wsgi:application` is not a valid
module for this project.

## Tests and checks

```powershell
python manage.py check
python manage.py test academy
```
