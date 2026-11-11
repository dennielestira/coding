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

- **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput`
- **Start Command:** `python manage.py migrate --noinput && python manage.py seed_content && exec gunicorn it_skills_academy.wsgi:application --bind 0.0.0.0:$PORT`

The start command applies migrations and loads starter content against the
runtime database before serving requests. Update the Render service's existing
Start Command and Build Command to these values, then redeploy. WhiteNoise
serves the collected CSS and JavaScript from `STATIC_ROOT`.

Set `DJANGO_SECRET_KEY` and `DJANGO_DEBUG=false` in the service's environment
variables. Render's `RENDER_EXTERNAL_HOSTNAME` is added to `ALLOWED_HOSTS`
automatically. Set `DJANGO_ALLOWED_HOSTS` to a comma-separated list if you also
use a custom domain. The WSGI application is
`it_skills_academy.wsgi:application`; `academy.wsgi:application` is not a valid
module for this project.

## Tests and checks

```powershell
python manage.py check
python manage.py test academy
```
