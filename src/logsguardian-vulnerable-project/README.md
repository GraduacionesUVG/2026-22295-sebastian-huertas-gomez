# Vulnerable Notes App

A deliberately vulnerable Node.js/Express web application for use as a baseline attack target during RASP library evaluation. **Do not deploy to production or expose to the internet.**

## Quick Start

```bash
docker compose up
```

The app is available at **http://localhost:3000** once the database is ready (health check takes ~10 seconds on first run). No additional steps required — schema and seed data are loaded automatically.

## Seed Credentials

| Username | Password  | Role  |
|----------|-----------|-------|
| admin    | admin123  | admin |
| alice    | alice123  | user  |
| bob      | bob123    | user  |

## Architecture

- **App:** Node.js 20 + Express 4 on port 3000
- **Database:** PostgreSQL 15 (internal, not exposed to host)
- **Sessions:** Cookie-based via express-session (no JWT)
- **Views:** EJS server-side rendering
- **File uploads:** multer, stored at `/app/uploads` inside the container

## Vulnerability Summary

See [VULNERABILITIES.md](./VULNERABILITIES.md) for exact endpoints, source file locations, and working `curl` exploit commands for all four vulnerability categories:

1. SQL Injection — `POST /login` and `GET /posts/search`
2. Stored XSS — `POST /profile` (bio) and `POST /posts` (post content)
3. Path Traversal — `GET /posts/:id/attachment?file=`
4. Command Injection — `POST /admin/ping`

## Resetting State

```bash
docker compose down -v && docker compose up
```

This removes all volumes and re-seeds the database from scratch.

## Adding logSguarDian (later phase)

The app exposes a plain `express()` instance at `src/app.js`. To mount logSguarDian as middleware in a later evaluation phase, add `app.use(logSguarDian())` in `src/app.js` before the route mounts — no other changes needed.
