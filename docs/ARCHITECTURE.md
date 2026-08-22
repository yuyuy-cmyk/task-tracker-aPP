# Architecture

## Overview

The Task Tracker uses a deliberately small client/server architecture.

```text
Browser
  |
  | HTTP/JSON
  v
FastAPI application (`app/main.py`)
  |
  +--> Pydantic validation (`app/models.py`)
  +--> status rules (`app/business_rules.py`)
  +--> in-memory storage (`app/storage.py`)
```

The browser frontend is a static `frontend/index.html` page using vanilla HTML, CSS, and JavaScript. It calls the FastAPI API running on port 8000. During local development the frontend is served on port 5500, which is included in the API CORS allow-list.

## Backend flow

1. FastAPI receives a request in `app/main.py`.
2. Pydantic validates request fields against `TaskCreate` or `TaskUpdate`.
3. Route-level business behavior such as filtering or missing-task handling is applied.
4. Status changes are checked by `validate_status_transition`.
5. `app/storage.py` creates, retrieves, updates, or deletes the in-memory `TaskResponse` object.
6. FastAPI serializes the validated response to JSON.

## Data model

A task contains an ID, title, description, status, priority, optional assignee, optional due date, tags, and created/updated timestamps. `is_overdue` is computed from the due date and status.

## Persistence decision

The current project intentionally uses an in-memory Python dictionary. This means data is lost when the backend process or container restarts. The final-release work preserves this design because replacing it with a database would be an unnecessary product/architecture rewrite for this assignment.

## Frontend

The frontend is intentionally build-free: one static HTML file contains the UI, styling, and JavaScript. This keeps the course project easy to run and inspect. Docker serves the file through Nginx; non-Docker development may use Python's built-in HTTP server.

## Deployment boundary

The repository provides development Docker support, not production deployment. There is no authentication, production database, multi-tenancy, notification system, or real-time service.
