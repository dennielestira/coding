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

## Use Supabase PostgreSQL

The app uses SQLite when `DATABASE_URL` is unset, and PostgreSQL when it is
set. To connect to Supabase, copy `.env.example` to `.env` and set
`DATABASE_URL` to the PostgreSQL connection URI from your Supabase project's
**Connect** dialog. Use a URI with SSL enabled (`sslmode=require`) and keep the
password private. The app loads `.env` locally; never commit it.

For a deployed app, add `DATABASE_URL` as a secret environment variable in the
hosting provider instead. `DB_CONN_MAX_AGE` controls the connection lifetime
in seconds and defaults to `0`, which is suitable for Supabase's transaction
pooler. After setting the URI, apply the schema and seed the starter content:

```powershell
python manage.py migrate
python manage.py seed_content
```

The existing local SQLite database is not copied automatically. If it contains
data you need to preserve, export/import that data separately before switching
the application to Supabase.

## Deploy on Vercel

Vercel's serverless filesystem is not a persistent database, so configure
Supabase PostgreSQL before deploying. In the Vercel project, open
**Settings → Environment Variables** and add `DATABASE_URL` with the PostgreSQL
URI from the Supabase project's **Connect** dialog. Enable it for each Vercel
environment you deploy (Production, Preview, and/or Development), then
redeploy. The app deliberately refuses to start on Vercel if `DATABASE_URL` is
missing instead of attempting to use a local SQLite file.

Run `python manage.py migrate` and `python manage.py seed_content` against that
same Supabase database once before serving the app. Do not put database
credentials in the repository or in the Vercel build command.

## Deploy on Render

Configure the Render web service with these commands:

- **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput`
- **Start Command:** `python manage.py migrate --noinput && python manage.py seed_content && exec gunicorn it_skills_academy.wsgi:application --bind 0.0.0.0:$PORT`

The start command applies migrations and loads starter content against the
runtime database before serving requests. Update the Render service's existing
Start Command and Build Command to these values, then redeploy. WhiteNoise
serves the collected CSS and JavaScript from `STATIC_ROOT`.

Set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=false`, and the Supabase `DATABASE_URL`
in the service's environment variables. Render's `RENDER_EXTERNAL_HOSTNAME` is
added to `ALLOWED_HOSTS` automatically. Set `DJANGO_ALLOWED_HOSTS` to a
comma-separated list if you also use a custom domain. The WSGI application is
`it_skills_academy.wsgi:application`; `academy.wsgi:application` is not a valid
module for this project.

## Tests and checks

```powershell
python manage.py check
python manage.py test academy
```
