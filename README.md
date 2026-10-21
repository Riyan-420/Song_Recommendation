# MusicMind — Personality-Based Song Recommendation

MusicMind is a Flask web app that recommends songs based on a user's personality. Users take a short
questionnaire (Big Five traits plus genre, energy, mood and lyrics preferences), and the app matches
those answers against trait-tagged songs in its catalogue. Admins manage songs, users and
notifications from a dashboard.

## Features

- Registration, login and profile management (Flask-Login, hashed passwords)
- Personality questionnaire that produces ranked song recommendations, which users can rate
- Admin dashboard: add/edit/delete songs and users, send notifications, restore deleted items ("Graveyard")
- Optional Firestore browser for admins (Firebase)
- Database migrations via Flask-Migrate / Alembic

## Tech stack

Python 3.11+, Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF, Flask-Migrate,
SQLite (default) or PostgreSQL, optional `firebase-admin`.

## Project layout

```
app.py              Application factory and entry point
config.py           Configuration (reads environment / .env)
extensions.py       Shared Flask extensions (db, login manager, migrate)
admin_utils.py      @admin_required decorator
create_admin.py     Creates the initial admin user
insert_songs.py     Seeds the song catalogue
models/             SQLAlchemy models (user, song, preference, recommendation, notification)
routes/             Blueprints: auth, recommendations, admin
forms/              Flask-WTF forms
templates/          Jinja2 templates (admin/ for the dashboard)
static/             CSS, JS, images, uploads
migrations/         Alembic migrations
```

## Getting started

```bash
git clone https://github.com/Riyan-420/Song_Recommendation.git
cd Song_Recommendation

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env            # then edit the values
```

### Configuration (`.env`)

| Variable | Purpose |
|---|---|
| `SECRET_KEY` | Flask session signing key (required in production) |
| `DATABASE_URL` | SQLAlchemy URL. Defaults to a local SQLite file `app.db`. PostgreSQL: `postgresql://user:pass@localhost:5432/music_recommendation` |
| `FIREBASE_KEY_PATH` | Optional path to a Firebase service-account JSON (defaults to `./firebase_key.json`) |
| `ADMIN_USERNAME`, `ADMIN_EMAIL`, `ADMIN_PASSWORD` | Used by `create_admin.py` |

### Set up the database, seed data and admin

```bash
python insert_songs.py     # load sample songs
python create_admin.py     # create the admin account from .env
```

Tables are created automatically on start-up. To use migrations instead, run `flask --app app db upgrade`.

### Run

```bash
python app.py
```

Open http://127.0.0.1:5000. The admin dashboard is at `/admin/dashboard`.

## Firebase (optional)

The admin-only page at `/admin/firebase-integration` talks to Firestore. To enable it, create a
service-account key in the Firebase console and save it as `firebase_key.json` in the project root
(or point `FIREBASE_KEY_PATH` at it). **Never commit this file** — it is listed in `.gitignore`.

## Security notes

- Secrets live in `.env` / environment variables only; `.env` and `firebase_key.json` are git-ignored.
- Set a strong, unique `SECRET_KEY` and admin password before deploying.
- Run with `debug=True` only in development.
