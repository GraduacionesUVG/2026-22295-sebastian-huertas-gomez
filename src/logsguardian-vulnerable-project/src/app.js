const express = require('express');
const session = require('express-session');
const path    = require('path');
const { logsguardian } = require('logsguardian');
const upload  = require('./middleware/upload');

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

// Parses multipart/form-data bodies (fields + files) before logsguardian's
// middleware runs. Previously logsguardian read req.body ahead of any
// multipart parsing, which only happened downstream in per-route multer
// instances - so multipart requests reached it with an empty body regardless
// of payload. Content-type routing is multer's own, so non-multipart
// requests pass through unchanged.
app.use(upload.any());

if (process.env.LOGSGUARDIAN_DISABLED !== 'true') {
  app.use(logsguardian({
    mode:      'block',
    // No modelDir override (was: path.join(__dirname, '../models')) -- uses
    // the middleware's own bundled models/ (DEFAULT_MODEL_DIR) instead, the
    // same ones `npm install logsguardian@0.1.1` actually ships. This is
    // specifically to test the real published package as a real user would
    // run it, not a locally-swapped model pair.
    dbPath:    process.env.LOGSGUARDIAN_DB_PATH || path.join(__dirname, '../logsguardian-events.db'),
    timeoutMs: 5000,
  }));
}

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

app.use('/',      authRoutes);
app.use('/posts', postsRoutes);
app.use('/',      profileRoutes);
app.use('/admin', adminRoutes);

app.use((req, res) => {
  res.status(404).render('error', {
    user:    req.session.user || null,
    status:  404,
    message: 'Page not found.',
  });
});

module.exports = app;
