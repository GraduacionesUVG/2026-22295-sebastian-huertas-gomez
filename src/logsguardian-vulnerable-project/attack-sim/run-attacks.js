// Fires each category's 100-payload set against its vulnerable endpoint and
// counts how many logsguardian blocks (403). Run with middleware active.
const fs = require('fs');
const path = require('path');

const BASE_URL = process.env.TARGET_URL || 'http://localhost:3000';

async function login(username, password) {
  const res = await fetch(`${BASE_URL}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ username, password }).toString(),
    redirect: 'manual',
  });
  const setCookie = res.headers.get('set-cookie');
  if (!setCookie) throw new Error(`login failed for ${username}: no set-cookie (status ${res.status})`);
  return setCookie.split(';')[0];
}

async function sendSqli(cookie, payload) {
  return fetch(`${BASE_URL}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ username: payload, password: 'x' }).toString(),
    redirect: 'manual',
  });
}

async function sendXss(cookie, payload) {
  return fetch(`${BASE_URL}/profile`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded', Cookie: cookie },
    body: new URLSearchParams({ bio: payload }).toString(),
    redirect: 'manual',
  });
}

async function sendPathTraversal(cookie, payload) {
  const url = `${BASE_URL}/posts/1/attachment?file=${encodeURIComponent(payload)}`;
  return fetch(url, { headers: { Cookie: cookie }, redirect: 'manual' });
}

async function sendCmdi(cookie, payload) {
  return fetch(`${BASE_URL}/admin/ping`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded', Cookie: cookie },
    body: new URLSearchParams({ host: payload }).toString(),
    redirect: 'manual',
  });
}

const CATEGORIES = {
  sqli: { sender: sendSqli, user: null },
  xss: { sender: sendXss, user: { username: 'alice', password: 'alice123' } },
  path_traversal: { sender: sendPathTraversal, user: { username: 'alice', password: 'alice123' } },
  cmdi: { sender: sendCmdi, user: { username: 'admin', password: 'admin123' } },
};

async function run() {
  const results = {};
  for (const [name, { sender, user }] of Object.entries(CATEGORIES)) {
    const payloads = JSON.parse(
      fs.readFileSync(path.join(__dirname, 'payloads', `${name}.json`), 'utf8')
    );
    const cookie = user ? await login(user.username, user.password) : null;
    let blocked = 0;
    const statusCounts = {};
    for (const payload of payloads) {
      const res = await sender(cookie, payload);
      statusCounts[res.status] = (statusCounts[res.status] || 0) + 1;
      if (res.status === 403) blocked++;
    }
    results[name] = { blocked, total: payloads.length, statusCounts };
    console.log(`${name}: ${blocked}/${payloads.length} blocked (${(blocked / payloads.length * 100).toFixed(1)}%)`, statusCounts);
  }
  fs.writeFileSync('/tmp/attack-results.json', JSON.stringify(results, null, 2));
}

run().catch((err) => {
  console.error(err);
  process.exit(1);
});
