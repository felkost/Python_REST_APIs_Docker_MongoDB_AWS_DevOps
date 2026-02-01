# Experimental DevOps Repo: Flask + MongoDB + Docker + GitHub (uv)

````md

This repository is an **experimental / learning project** to practice how these technologies work together:

- **Flask** (Python REST API)
- **MongoDB** (database in a Docker container)
- **Docker + Docker Compose** (run API + DB as one stack)
- **Git + GitHub** (feature branches, commits, Pull Requests)
- **uv** (modern Python environment + dependency manager)

Goal: build a **reproducible** setup that a beginner can run locally and understand step by step.

---

## ✅ Security note (no passwords in Git)

This project uses environment variables for secrets.

**Do NOT commit these files:**
- `.env`
- `.venv/`

Add them to:
- `.gitignore` (for `.env`, `.venv/`)
- `.dockerignore` (for `.env`, optional `.flaskenv`)

The README below uses **placeholders only** (no real passwords, no personal data).

---

## Tech stack

- **Python** with **uv**
- **Flask** for API routes
- **MongoDB** (official Docker image)
- **Docker Compose** for orchestration, network, volumes, healthcheck
- **GitHub** workflow: branch → commit → push → Pull Request

---

## Typical structure

> Names can differ in your repo. The key idea: Flask app lives inside `src/` as a Python package.

- `src/<your_package>/app.py` — Flask application
- `compose.yaml` — Docker Compose stack (`api` + `mongodb`)
- `mongo-init.js` — Mongo initialization script (create DB user)
- `.env` — environment variables (NOT committed)
- `pyproject.toml` + `uv.lock` + `.python-version` — reproducible Python setup

---

## Quick start (Docker Compose)

### 1) Create `.env` (local only)

Create a file `.env` in the repo root.

Use **safe placeholders** like this:

```env
# Mongo root user (only for container initialization)
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=change_me_root_password

# App database + app user
MONGO_APP_DB=appdb
MONGO_APP_USER=appuser
MONGO_APP_PASSWORD=change_me_app_password

# Connection string for Flask (service name "mongodb" = Docker DNS)
MONGO_URI=mongodb://appuser:change_me_app_password@mongodb:27017/appdb?authSource=appdb
````

**Important**

* Never share real passwords in screenshots, issues, or commits.
* If you need to publish the repo, consider adding `.env.example` with placeholders (no secrets).

---

### 2) Build and run the stack

```bash
docker compose up -d --build
```

Check containers:

```bash
docker compose ps
docker compose logs -f api
docker compose logs -f mongodb
```

Expected:

* `mongodb` → `Up (healthy)` (if healthcheck is configured)
* `api` → `Up`

---

### 3) Test the API

Example request (your endpoints can be different):

```bash
curl -X POST http://localhost:5000/inc \
  -H "Content-Type: application/json" \
  -d '{"x": 41}'
```

---

### 4) Check that data is stored in MongoDB (optional)

Enter Mongo shell:

```bash
docker exec -it mongodb mongosh -u admin -p "<root_password_here>" admin
```

> Tip: do NOT type real passwords in public logs or recordings.

Inside `mongosh`:

```js
use appdb
db.inc_calls.find().sort({_id:-1}).limit(5)
```

Exit:

```js
exit()
```

---

### 5) Restart without losing data (volumes)

Stop containers (volume stays):

```bash
docker compose down
```

Start again:

```bash
docker compose up -d
```

**Data should still exist** because MongoDB stores files in `/data/db`, mapped to a named volume.

⚠️ If you run:

```bash
docker compose down -v
```

the volume is removed and the database becomes clean (data will be lost).

---

## Python environment with uv (local dev)

### 1) Install dependencies from lock file

In repo root (where `pyproject.toml` is):

```bash
uv sync
```

This creates/updates `.venv` and installs exact versions from `uv.lock`.

### 2) Run the app locally (without Docker)

If your Flask app is an **app object**:

```bash
uv run flask --app <your_package>.app run --debug
```

If you use an **app factory** `create_app()`:

```bash
uv run flask --app <your_package>.app:create_app run --debug
```

> Replace `<your_package>` with your real package name inside `src/`.

---

## Git + GitHub workflow (Pull Request)

### 0) Check current branch

```bash
git status
git branch --show-current
```

### 1) Create a feature branch

```bash
git switch -c feat/<topic>
```

Examples:

* `feat/mongo`
* `feat/flask-healthcheck`
* `fix/docker-env-vars`

### 2) Stage and commit changes

```bash
git add -A
git diff --cached
git commit -m "Add MongoDB via Docker Compose"
```

### 3) Push branch

```bash
git push -u origin feat/<topic>
```

### 4) Open a Pull Request on GitHub

Base: `main`
Compare: `feat/<topic>`

Merge strategy recommendation for learning repos:

* **Squash and merge** (clean main history)

---

## Update your feature branch when `main` changed

### Option A (safe): merge `main` into feature

```bash
git switch feat/<topic>
git fetch origin
git merge origin/main
git push
```

### Option B (clean history): rebase feature on `main`

```bash
git switch feat/<topic>
git fetch origin
git rebase origin/main
git push --force-with-lease
```

**Note:** Rebase can require `force-with-lease`. If you are not sure about repo rules, use merge.

---

## What to commit / what not to commit

✅ Commit:

* `pyproject.toml`
* `uv.lock`
* `.python-version`
* `compose.yaml`
* `mongo-init.js`
* code in `src/`

❌ Do NOT commit:

* `.env`
* `.venv/`
* `__pycache__/`
* `.pytest_cache/`

---

## Project idea (real-life use scenario)

1. You start the stack with Docker Compose.
2. A client (curl / Postman / frontend) calls API endpoints.
3. Flask validates input, calculates a result, and writes a document to MongoDB.
4. MongoDB stores data in a named volume, so container restarts are safe.
5. You use logs to monitor the system and GitHub PRs to track changes.

---

## License

Learning / experimental repository.
