-- Realistic-data-volume seed for the "volume" latency scenario.
--
-- Adds 2000 generated rows on top of the 10 rows already inserted by
-- db/init.sql, for a total of 2010 rows in `posts` - matching the row count
-- cited in docs/vulnerable-app-evaluation/config2-latency-evaluation.md
-- (sibling repo, read-only) as the scale at which the relative Delta p95
-- dropped to +70.2%. NOTE: that document reports the *result* of a
-- 2010-row seed but does not document the seeding method itself (verified:
-- no seed script, SQL, or generation method for it exists anywhere in the
-- sibling repo's history or docs at the time this file was written) - this
-- script is a new, independent implementation designed to reach the same
-- total row count (10 + 2000 = 2010), not a copy of a pre-existing method.
--
-- Not wired into db/init.sql / docker-entrypoint-initdb.d on purpose: the
-- normal-load and attack-load scenarios should run against the small
-- (10-row) seed exactly as before. This script is applied on demand, after
-- the stack is already up, only for the "volume" scenario - see
-- attack-sim/seed-large-dataset.sh.
--
-- user_id cycles through the 3 seeded users (1=admin, 2=alice, 3=bob) so
-- ownership/edit-permission checks in src/routes/posts.js still exercise
-- realistically (not every generated post belongs to the same user).
-- Content length is deliberately non-trivial (repeated lorem ipsum, ~300
-- chars) so `GET /posts` renders a realistic amount of HTML per row rather
-- than trivially short strings that would understate real-world render
-- cost.
INSERT INTO posts (user_id, title, content)
SELECT
  ((gs % 3) + 1) AS user_id,
  'Generated Post #' || gs AS title,
  repeat('Lorem ipsum dolor sit amet, consectetur adipiscing elit. ', 5)
    || 'Entry number ' || gs || '.' AS content
FROM generate_series(1, 2000) AS gs;
