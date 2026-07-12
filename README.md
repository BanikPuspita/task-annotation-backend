# TaskFlow — Backend

Django REST API powering the TaskFlow fullstack app — task management, image uploads, and polygon annotation persistence. Built as part of the 404 Project Fullstack Engineering task.

---

## Live Demo

| Resource | Link |
|----------|------|
| **Hosted API (Render)** | https://task-annotation-backend.onrender.com/api |
| **Django Admin** | https://task-annotation-backend.onrender.com/admin/ |
| **GitHub Repository** | https://github.com/BanikPuspita/task-annotation-backend |
| **Frontend App (Vercel)** | https://task-annotation-frontend-gilt.vercel.app |
| **Frontend Repo** | https://github.com/BanikPuspita/task-annotation-frontend |

### Demo Login Credentials

| Field | Value |
|-------|-------|
| **Email** | `admin@example.com` |
| **Password** | `admin123` |

Use these credentials in the frontend login page or Django admin.

---

## Features

### Authentication
- Email + password login via JWT (`access` + `refresh` tokens)
- Automatic token refresh endpoint
- All task, image, and annotation endpoints require authentication

### Task Management API
- CRUD operations for tasks (user-scoped)
- Filter tasks by date: `GET /api/tasks/?date=YYYY-MM-DD`
- Fields: title, description, priority, status, due_date, task_date, tags

### Image Upload API
- Multipart file upload to **Cloudinary** (cloud storage)
- Returns `image_url` for frontend display
- User-scoped image listing

### Annotation API
- Create, list, and delete polygon annotations per image
- Filter by image: `GET /api/annotations/?image=<id>`
- Polygon coordinates stored as JSON

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.11 | Runtime |
| Django 5.2 | Web framework |
| Django REST Framework | REST API |
| djangorestframework-simplejwt | JWT authentication |
| django-cors-headers | CORS for Vercel frontend |
| Cloudinary | Cloud image storage |
| SQLite | Database (local & Render) |
| Gunicorn + WhiteNoise | Production server & static files |

---

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/api/login/` | Public | Login with email & password |
| `POST` | `/api/token/refresh/` | Public | Refresh JWT access token |
| `GET` | `/api/profile/` | JWT | Get current user profile |
| `GET`, `POST` | `/api/tasks/` | JWT | List / create tasks |
| `GET`, `PATCH`, `DELETE` | `/api/tasks/<id>/` | JWT | Retrieve / update / delete task |
| `GET`, `POST` | `/api/images/` | JWT | List / upload images |
| `GET`, `POST` | `/api/annotations/` | JWT | List / create annotations |
| `GET`, `DELETE` | `/api/annotations/<id>/` | JWT | Retrieve / delete annotation |

---

## Database Models

```
User (Django built-in)
  ├── Task     (title, description, priority, status, due_date, task_date, tags)
  ├── Image    (title, image_url, public_id — stored on Cloudinary)
  └── Annotation (image FK, label, polygon JSON)
```

All models are user-scoped — each user only sees their own data.

---

## Project Structure

```
backend/
├── api/
│   ├── models.py              # Task, Image, Annotation models
│   ├── views.py               # API views (CRUD + Cloudinary upload)
│   ├── urls.py                # API route definitions
│   ├── admin.py               # Django admin registration
│   ├── serializers/           # DRF serializers
│   └── management/commands/
│       └── seed_data.py       # Sample data seeder
├── config/
│   ├── settings.py            # Django settings (CORS, JWT, Cloudinary)
│   └── urls.py                # Root URL config
├── build.sh                   # Render build script
├── requirements.txt
└── manage.py
```

---

## Challenges & How I Overcame Them

### Villain 1: Image storage on a cloud host with no persistent filesystem
Render's filesystem is ephemeral — uploaded image files would disappear on redeploy if stored locally with Django's `ImageField`.

**How I won:** Integrated **Cloudinary** for cloud image storage. The API uploads files directly via `cloudinary.uploader.upload()` and stores the returned `secure_url` and `public_id` in the database. Images persist independently of server restarts.

### Villain 2: CORS blocking frontend requests
The Vercel-hosted frontend couldn't communicate with the Render backend due to cross-origin restrictions.

**How I won:** Configured `django-cors-headers` with `CORS_ALLOWED_ORIGINS` including both `http://localhost:5173` (dev) and `https://task-annotation-frontend-gilt.vercel.app` (production). Placed `CorsMiddleware` first in the middleware stack.

### Villain 3: Local vs hosted database confusion
Data created via Django admin locally didn't appear in the hosted frontend, causing confusion about whether the app was working.

**How I won:** Documented clearly that local `db.sqlite3` and Render's database are separate. Production uses only the Render API and database. Added `.env.example` files for both projects to make environment setup explicit.

### Villain 4: JWT authentication with DRF
Setting up email-based login (instead of username) with JWT tokens required custom serializer logic.

**How I won:** Built `EmailLoginSerializer` that looks up users by email, validates the password, and returns JWT `access`/`refresh` tokens plus user info. Frontend stores tokens in `localStorage` and attaches them via Axios interceptors.

### Villain 5: `cloudinary_storage` breaking the Render build
The `django-cloudinary-storage` package caused Python compatibility issues during deployment.

**How I won:** Removed `cloudinary_storage` from `INSTALLED_APPS` and handled uploads directly in the view using the `cloudinary` Python SDK — simpler and more reliable.

### Villain 6: Tasks and images disappearing after some time
User-created tasks and images would vanish from both the frontend and Django admin after a while.

**Root cause (two issues):**
1. `build.sh` ran `seed_data` on every deploy, which called `Task.objects.all().delete()` — wiping all user data.
2. SQLite on Render uses an ephemeral filesystem — the database file resets when the service restarts or redeploys.

**How I won:**
- Removed `seed_data` from the production build script.
- Made `seed_data` safe — it only runs on an empty database and never deletes existing records.
- Added PostgreSQL support via `DATABASE_URL` so production can use Render's persistent PostgreSQL instead of SQLite.

---

## Prerequisites

| Tool | Version |
|------|---------|
| **Python** | 3.11.11 (3.10+ supported) |
| **pip** | Latest |
| **Cloudinary account** | Free tier works (for image uploads) |

---

## How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/BanikPuspita/task-annotation-backend.git
cd task-annotation-backend
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root (use `.env.example` as reference):

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
CORS_ALLOWED_ORIGINS=http://localhost:5173

# Required for image uploads
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

### 5. Run database migrations

```bash
python manage.py migrate
```

### 6. Seed sample data (optional)

```bash
python manage.py seed_data
```

This creates the demo user (`admin@example.com` / `admin123`) and sample tasks.

### 7. Start the development server

```bash
python manage.py runserver
```

API available at http://127.0.0.1:8000/api/
Django admin at http://127.0.0.1:8000/admin/

### 8. Connect the frontend

In the frontend `.env`, set:

```env
VITE_API_URL=http://127.0.0.1:8000/api
```

Then run `npm run dev` in the frontend folder.

---

## Deployment (Render)

### Step 1: Create a PostgreSQL database (required for data persistence)

1. In Render dashboard → **New** → **PostgreSQL**
2. Name it (e.g. `taskflow-db`) and create it
3. Copy the **Internal Database URL**

> **Important:** Without PostgreSQL, SQLite data on Render will be lost on every redeploy or restart.

### Step 2: Deploy the web service

1. Push code to GitHub
2. Create a new **Web Service** on Render linked to the backend repo
3. Set environment variables:

   | Variable | Value |
   |----------|-------|
   | `SECRET_KEY` | A secure random string |
   | `DEBUG` | `False` |
   | `ALLOWED_HOSTS` | `task-annotation-backend.onrender.com` |
   | `CORS_ALLOWED_ORIGINS` | `https://task-annotation-frontend-gilt.vercel.app` |
   | `DATABASE_URL` | Paste the PostgreSQL Internal Database URL |
   | `CLOUDINARY_CLOUD_NAME` | Your Cloudinary cloud name |
   | `CLOUDINARY_API_KEY` | Your Cloudinary API key |
   | `CLOUDINARY_API_SECRET` | Your Cloudinary API secret |

4. Build command: `./build.sh`
5. Start command: `python -m gunicorn config.wsgi:application`

### Step 3: Seed sample data (one-time, optional)

After first deploy, open the Render **Shell** and run:

```bash
python manage.py seed_data
```

This only adds sample tasks if the database is empty — it will never delete your existing data.

---

## Management Commands

| Command | Description |
|---------|-------------|
| `python manage.py migrate` | Apply database migrations |
| `python manage.py seed_data` | Create demo user and sample tasks (only if DB is empty) |
| `python manage.py createsuperuser` | Create an admin user manually |
| `python manage.py runserver` | Start local dev server |
