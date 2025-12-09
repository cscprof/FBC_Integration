## Purpose
Short, practical guidance for AI coding agents working on this Flask-based UI project so they can be productive immediately.

## Big picture
- Single-process Flask app defined in `app.py`. Routes render Jinja templates found in `templates/` and static assets live under `static/`.
- The app uses `pymysql` to read an `events` table (see `app.py` -> `/events` route). There is no ORM; raw SQL + connection handling is used.

## Where to look first (quick tour)
- `app.py` — entrypoint, routes, DB connection config (variable `db_config`). Example: `/events` executes `SELECT * FROM events` and passes `events` to `events.html`.
- `templates/layout.html` — base template (includes Bulma and Bootstrap CDNs). Most pages `extend 'layout.html'`.
- `templates/index.html`, `templates/events.html`, `templates/calendar.html` — page examples. `calendar.html` uses a client-side `calendar.js` and CSS in `static/css/calendar.css`.
- `static/css/` — contains `styles.css` and `calendar.css` for page styles.

## Project-specific patterns and conventions
- Templating: Jinja2 `extends` / `block` pattern (see `layout.html`). Use `url_for('static', filename=...)` when adding or fixing static asset links (layout.html already uses it for `styles.css`).
- Static assets: prefer `{{ url_for('static', filename='js/calendar.js') }}` and similar rather than bare `calendar.js` or `calendar.css` to ensure correct static path resolution.
- DB access: the project uses `pymysql` with an inline `db_config` dict in `app.py`. Connections are opened per-request and closed in a `finally` block — follow that pattern when adding new DB access. Keep SQL simple and parameterized to avoid injection.
- Error handling: routes return error strings on exceptions (e.g., `return f"Error: {err}"`). If you modify behavior, keep failures visible during local development but avoid leaking secrets in production.

## How to run locally (developer workflow)
- This app is runnable directly with Python (it has `if __name__ == '__main__': app.run(debug=True)` in `app.py`). On Windows PowerShell:

```powershell
# create a virtual env and activate (optional)
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install flask pymysql
python app.py
```

- Alternatively, set `FLASK_APP=app.py` and run `flask run`, but the simplest is `python app.py` because the file already starts the server.

## Dependency notes
- There is no `requirements.txt` in the repo. When adding packages, update `requirements.txt` (example: `flask==x.y.z`, `pymysql==x.y.z`).

## Common edits you'll be asked to do (and how to do them here)
- Add a new route that returns a template: follow the `@app.route('/...')` + `def name(): return render_template('foo.html')` pattern.
- Query the DB: use the `db_config` dict and follow the `events()` example — open connection with `pymysql.connect(**db_config)`, create a cursor, `execute`, `fetchall()`, and close resources in `finally`.
- Fix static links: update templates to use `{{ url_for('static', filename='path') }}` rather than relative file names. Example change: replace `<script src="calendar.js"></script>` with `<script src="{{ url_for('static', filename='js/calendar.js') }}"></script>`.

## Examples from this repo
- DB pattern (from `app.py`):

```py
conn = pymysql.connect(**db_config)
cursor = conn.cursor()
cursor.execute("SELECT * FROM events")
events = cursor.fetchall()
```

- Template pattern (from `calendar.html` and `layout.html`):

```jinja
{% extends 'layout.html' %}
{% block content %}
  ...
{% endblock %}
```

## Safety & changes to credentials
- `db_config` currently contains host/user/password/database values inside `app.py`. If you need to change connection details, prefer using environment variables or a config file and avoid committing secrets. If you must change `app.py` for local debugging, note that credentials are currently stored in plaintext.

## Tests, linting, and CI
- There are no tests or CI configs in the repo. Keep changes small and run the app locally to verify routes and templates. If you add dependencies or scripts, update `requirements.txt` and document run steps in a top-level `README.md`.

## When in doubt
- Run the app locally, open `/` and `/events` first. For DB failures, check `db_config` and whether a MySQL instance with the expected schema exists. Prefer minimal, localized changes and preserve the existing patterns.

---
If you'd like, I can (1) add a `requirements.txt` with the minimal deps, (2) convert the inline static references to `url_for` usages, or (3) extract DB config to environment variables—tell me which and I'll make the changes.
