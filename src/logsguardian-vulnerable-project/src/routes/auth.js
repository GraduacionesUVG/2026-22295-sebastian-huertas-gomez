const express = require('express');
const router  = express.Router();
const db      = require('../db');

// GET /login
router.get('/login', (req, res) => {
  if (req.session.user) return res.redirect('/posts');
  res.render('login', { user: null, error: null });
});

// POST /login  —  VULNERABLE: SQL Injection via string concatenation
// Allows authentication bypass with: username = ' OR '1'='1' --
router.post('/login', async (req, res) => {
  const { username, password } = req.body;
  try {
    // VULNERABLE: inputs embedded directly into the query string
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
