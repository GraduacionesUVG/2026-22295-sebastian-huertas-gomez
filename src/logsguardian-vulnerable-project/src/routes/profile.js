const express = require('express');
const router  = express.Router();
const db      = require('../db');
const { requireLogin } = require('../middleware/auth');

// GET /profile
router.get('/profile', requireLogin, async (req, res) => {
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

// POST /profile  —  stores raw bio without sanitization (XSS rendered in template via <%- %>)
router.post('/profile', requireLogin, async (req, res) => {
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

// GET /users/:id  —  viewing another user's profile triggers their stored XSS payload
router.get('/users/:id', requireLogin, async (req, res) => {
  try {
    const result = await db.query(
      'SELECT id, username, bio, role, created_at FROM users WHERE id = $1',
      [req.params.id]
    );
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
