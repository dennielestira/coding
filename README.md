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

## Tests and checks

```powershell
python manage.py check
python manage.py test academy
```
