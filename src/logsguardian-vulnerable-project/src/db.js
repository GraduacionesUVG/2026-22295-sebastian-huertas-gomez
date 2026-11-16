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
