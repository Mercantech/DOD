const express = require('express');
const path = require('path');
const os = require('os');
const { Client } = require('pg');

const app = express();
const PORT = process.env.PORT || 3000;

// Statisk frontend
app.use(express.static(path.join(__dirname, 'public')));

function getDbStatus() {
  const host = process.env.NODE_DB_HOST;
  if (!host) return Promise.resolve({ ok: false, message: 'NODE_DB_HOST ikke sat' });
  const client = new Client({
    host,
    port: process.env.NODE_DB_PORT || 5432,
    user: process.env.NODE_DB_USER || 'proxi',
    password: process.env.NODE_DB_PASSWORD || 'proxi',
    database: process.env.NODE_DB_NAME || 'proxi',
    connectionTimeoutMillis: 3000,
  });
  return client
    .connect()
    .then(() => client.query('SELECT 1'))
    .then(() => ({ ok: true, message: 'Forbundet til Postgres' }))
    .catch((err) => ({ ok: false, message: err.message || 'Fejl' }))
    .finally(() => client.end());
}

// API: hvilken server/host + IP vi kører på + DB-status
app.get('/api/whoami', (req, res) => {
  const ifaces = os.networkInterfaces();
  let ip = process.env.NODE_IP || '127.0.0.1';
  if (!process.env.NODE_IP) {
    for (const name of Object.keys(ifaces)) {
      for (const iface of ifaces[name]) {
        if (iface.family === 'IPv4' && !iface.internal) {
          ip = iface.address;
          break;
        }
      }
    }
  }
  getDbStatus().then((db) => {
    res.json({
      hostname: process.env.HOSTNAME || os.hostname(),
      ip,
      platform: os.platform(),
      db,
    });
  });
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Proxi demo listening on 0.0.0.0:${PORT}`);
});
