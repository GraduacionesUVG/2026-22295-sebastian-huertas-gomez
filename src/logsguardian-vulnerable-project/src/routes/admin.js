const express  = require('express');
const router   = express.Router();
const db       = require('../db');
const { exec } = require('child_process');
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

// POST /admin/ping  —  VULNERABLE: Command Injection via exec + string concatenation
// Allows arbitrary command execution with: host = "127.0.0.1 ; cat /etc/passwd"
router.post('/ping', requireAdmin, (req, res) => {
  const { host } = req.body;
  if (!host) {
    return res.status(400).json({ error: 'Missing host parameter.' });
  }
  // VULNERABLE: host value embedded directly in shell command string
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
