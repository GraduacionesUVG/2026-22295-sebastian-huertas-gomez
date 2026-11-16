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
  ('admin', 'admin123', 'Site administrator. Manages the platform.', 'admin'),
  ('alice', 'alice123', 'Writer and coffee enthusiast.',              'user'),
  ('bob',   'bob123',   'Developer by day, gamer by night.',         'user')
ON CONFLICT (username) DO NOTHING;

-- Seed posts
INSERT INTO posts (user_id, title, content) VALUES
  (2, 'My First Post',       'Hello world! This is Alice writing her first note on this platform.'),
  (2, 'Coffee Brewing Tips', 'The perfect espresso requires 9 bars of pressure and 25-30 seconds of extraction time.'),
  (2, 'Book Review: Dune',   'Frank Herbert''s world-building is unparalleled. The ecology of Arrakis feels real.'),
  (3, 'Vim vs Emacs',        'After years of debate I settled on Vim. Muscle memory wins.'),
  (3, 'Docker Networking',   'Bridge networks work for most cases but host mode cuts latency significantly.'),
  (3, 'My Gaming Setup',     'RTX 4090, 4K 144Hz monitor. Overkill? Maybe. Worth it? Absolutely.'),
  (1, 'Platform Guidelines', 'Please keep content respectful. Violations will result in account suspension.'),
  (1, 'Maintenance Window',  'Scheduled downtime on Sunday 02:00-04:00 UTC for database migration.'),
  (2, 'Productivity Hacks',  'Pomodoro technique changed my life. 25 minutes focus, 5 minute break.'),
  (3, 'Weekend Project',     'Built a small CLI tool in Go to parse nginx logs. Open sourcing soon.')
ON CONFLICT DO NOTHING;
