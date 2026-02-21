(function () {
  const hostEl = document.getElementById('host');
  const ipEl = document.getElementById('ip');
  const dbEl = document.getElementById('db');

  fetch('/api/whoami')
    .then(function (r) { return r.json(); })
    .then(function (data) {
      hostEl.textContent = data.hostname || '—';
      ipEl.textContent = data.ip || '—';
      if (data.db) {
        dbEl.textContent = 'DB: ' + (data.db.ok ? '✓ ' + data.db.message : '✗ ' + data.db.message);
        dbEl.className = 'db ' + (data.db.ok ? 'ok' : 'error');
      } else {
        dbEl.textContent = 'DB: —';
      }
    })
    .catch(function () {
      hostEl.textContent = '—';
      ipEl.textContent = 'Kunne ikke hente node';
      dbEl.textContent = 'DB: —';
    });
})();
