---
tags:
  - dod
  - nginx-https
  - nginx-https/nginx
---

# Nginx – reverse proxy

> **Dybere end dagens teori:** Videresende trafik til en app (fx Node, .NET) på port 3000/5000. Dag-note: [[../Noter/DoD - Pensum/Dag-04-Nginx-og-HTTPS]]. Grundlæggende: [[Nginx-grundlæggende]].

---

## Hvad er en reverse proxy?

En **reverse proxy** modtager klienters forespørgsler og sender dem videre til en eller flere **backends** (fx jeres app på port 3000). Klienten taler kun med Nginx; den ved ikke at appen kører bagved. Nginx kan samtidig håndtere SSL og statiske filer.

---

## proxy_pass – grundlæggende

```nginx
server {
    listen 80;
    server_name api.jeresprojekt.mercantec.tech;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

- **proxy_pass:** Nginx videresender til `http://127.0.0.1:3000` (jeres app).
- **proxy_set_header Host:** Appen får den rigtige Host-header (vigtigt for virtuelle hosts og redirects).
- **X-Real-IP / X-Forwarded-For:** Appen ser klientens rigtige IP (ellers ser den Nginx’ IP).
- **X-Forwarded-Proto:** Appen ved om request kom ind som HTTP eller HTTPS – vigtigt når Nginx terminerer SSL.

---

## Statisk + API under samme domæne

```nginx
location / {
    root /var/www/jeresprojekt;
    try_files $uri $uri/ @app;
}
location @app {
    proxy_pass http://127.0.0.1:3000;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

Først forsøges statiske filer; hvis ikke fundet, sendes request til appen.

---

## WebSocket (valgfrit)

Hvis appen bruger WebSocket, tilføj:

```nginx
proxy_http_version 1.1;
proxy_set_header Upgrade $http_upgrade;
proxy_set_header Connection "upgrade";
proxy_set_header Host $host;
```

Se [[Fejlsøgning-Nginx]] ved 502 eller forbindelsesfejl.
