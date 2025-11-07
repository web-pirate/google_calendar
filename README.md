# 📅 Google-like Calendar (Django + FullCalendar)

[![Django](https://img.shields.io/badge/Django-5.2.8-%230092bf)](https://www.djangoproject.com/)
[![FullCalendar](https://img.shields.io/badge/FullCalendar-6.x-orange)](https://fullcalendar.io/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-blue)](https://getbootstrap.com/)

A Google-Calendar inspired web app built with Django (backend), FullCalendar (frontend), and Bootstrap 5 for UI. This repo demonstrates event CRUD, multi-calendar sources, holiday import (Nager.Date), and weather lookup (Open-Meteo by default).

Quick links

- Live UI templates: core/templates/core/calendar.html and core/templates/test.html
- Backend endpoints: core.views (events_list, event_create, event_update, event_delete)
- Settings: googleCalender/settings.py

Why this project

- Lightweight calendar demo suitable for learning integrations: calendars, weather, public holidays.
- Minimal backend API to serve FullCalendar.
- Extensible: add authentication, recurring events, external calendar sync.

Getting started (local)

1. Clone:

```bash
git clone <repo>
cd c:\Users\Yamraj\Desktop\pcode\googleCalender
```

2. Create & activate virtualenv, install Django (project uses only Django by default):

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install django
```

3. Apply migrations and create superuser:

```bash
python manage.py migrate
python manage.py createsuperuser
# supply username/password — this user will appear in templates if you log in
```

4. Run dev server:

```bash
python manage.py runserver
# Open http://127.0.0.1:8000/
```

Environment & configuration

- Database: settings.py is configured for PostgreSQL by default (DATABASES). For quick testing you can switch to SQLite by replacing DATABASES with the commented SQLite block.
- Timezone: TIME_ZONE is `UTC` in settings.py. Adjust if needed.
- Weather: code uses Open-Meteo (no API key) and default latitude/longitude:
  - DEFAULT_LAT = 28.7041 (Delhi)
  - DEFAULT_LON = 77.1025
    Change in templates/scripts where these constants appear if you want other defaults.
- Holidays: Nager.Date public holidays API is used:
  - URL: https://date.nager.at/api/v3/PublicHolidays/{year}/IN
    No API key required.

Key files & responsibilities

- core/views.py — Django views exposing JSON endpoints:

  - events_list: GET events between start/end query parameters
  - event_create: POST to create events
  - event_update: PUT/PATCH to update events
  - event_delete: DELETE to remove events
    These endpoints are consumed by the frontend FullCalendar instance.

- core/templates/core/calendar.html — main UI for authenticated usage:

  - Mini-calendar in the sidebar (FullCalendar instance)
  - Main calendar (FullCalendar) with event CRUD modal
  - Weather card and holiday logic
  - Theme/dark-mode toggles

- core/templates/test.html — alternate demo template (works standalone in templates directory)

- googleCalender/settings.py — Django settings (DB, apps, middleware, templates). Update DB credentials here for production.

Icons and visuals

- Bootstrap Icons are already included in templates via CDN:

```html
<link
  href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css"
  rel="stylesheet"
/>
```

- Use icons in templates:

```html
<i class="bi bi-person-circle"></i>
<!-- person icon -->
<i class="bi bi-calendar-day"></i>
<!-- calendar icon -->
```

- You can also add emoji inline for quick visual cues (used for holidays: "🎉").

How login/superuser display works

- Templates include Django's `user` context (context processor enabled in settings). After you create a superuser (createsuperuser) and log in, `{{ user.username }}` will show in the navbar where templates render user info.
- If you don't have login flow yet, you can log in via `/admin/` to create sessions, or add simple links to Django auth views:
  - `path('accounts/login/', django.contrib.auth.views.LoginView.as_view(), name='login')`

Tips & troubleshooting

- Events disappear after custom JS changes: ensure you do not replace FullCalendar's event sources unintentionally — prefer addEventSource/remove or calendar.addEvent rather than calendar.render() multiple times.

- Weather: Open-Meteo provides forecast per-day; ensure date string format is YYYY-MM-DD.

Development notes (implementation highlights)

- Frontend uses two FullCalendar instances (mini + main) and synchronizes navigation.
- Weather uses Open-Meteo for daily high/low + basic weather code mapping.
- Holidays are fetched from Nager.Date per-year and added as all-day, non-editable events.
- Events are persisted via POST/PUT/DELETE against Django views returning JSON.

Future improvements

- Add full Django auth views and require login for calendar manipulation.
- Persist calendar sources per-user and add sharing/permissions.
- Implement recurring events parsing (rrule) and conflict detection.
- Add server-side caching for holiday API responses.
- Integrate Google Calendar / Microsoft sync.

Contribution

1. Fork
2. Create branch
3. Open PR with tests/description

License

- MIT

Contact

- Project owner: local developer (this is a demo local project)
