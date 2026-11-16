const express = require('express');
const router  = express.Router();
const db      = require('../db');
const path    = require('path');
const fs      = require('fs');
const { requireLogin } = require('../middleware/auth');

const UPLOAD_DIR = process.env.UPLOAD_DIR || path.join(__dirname, '../../uploads');

// Multipart bodies are already parsed globally in app.js (ahead of
// logsguardian) - req.files/req.body are populated by the time requests
// reach these routes, so no per-route multer instance runs here.
function findUploadedFile(req, fieldname) {
  return (req.files || []).find((f) => f.fieldname === fieldname) || null;
}

// GET /posts
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

// GET /posts/search?q=  —  VULNERABLE: SQL Injection via string concatenation
// Allows UNION-based data extraction with: ' UNION SELECT ...--
router.get('/search', requireLogin, async (req, res) => {
  const q = req.query.q || '';
  try {
    // VULNERABLE: q embedded directly in the LIKE clauses
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
router.post('/', requireLogin, async (req, res) => {
  const { title, content } = req.body;
  if (!title || !content) {
    return res.status(400).render('posts/new', { user: req.session.user, error: 'Title and content required.' });
  }
  const attachmentFile = findUploadedFile(req, 'attachment');
  const attachment = attachmentFile ? attachmentFile.filename : null;
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

// POST /posts/:id/attachment — upload a file
router.post('/:id/attachment', requireLogin, async (req, res) => {
  const file = findUploadedFile(req, 'attachment');
  if (!file) {
    return res.status(400).render('error', { user: req.session.user, status: 400, message: 'No file provided.' });
  }
  try {
    await db.query('UPDATE posts SET attachment = $1 WHERE id = $2', [file.filename, req.params.id]);
    res.redirect(`/posts/${req.params.id}`);
  } catch (err) {
    console.error(err);
    res.status(500).render('error', { user: req.session.user, status: 500, message: 'Internal server error.' });
  }
});

// GET /posts/:id/attachment?file=  —  VULNERABLE: Path Traversal
// Allows reading arbitrary files with: ?file=../../../etc/passwd
router.get('/:id/attachment', requireLogin, (req, res) => {
  const file = req.query.file;
  if (!file) {
    return res.status(400).json({ error: 'Missing file parameter.' });
  }
  // VULNERABLE: path.join resolves .. sequences but does not prevent escaping UPLOAD_DIR
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
