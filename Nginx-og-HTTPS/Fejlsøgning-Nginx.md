---
tags:
  - dod
  - nginx-https
  - nginx-https/nginx
---

# Fejlsøgning – Nginx

> **Dybere end dagens teori:** Logs og typiske fejl. Dag-note: [[../Noter/DoD - Pensum/Dag-04-Nginx-og-HTTPS]]. Grundlæggende: [[Nginx-grundlæggende]]. SSL: [[Lets-Encrypt-og-SSL]].

---

## Logs

- **Tilgangslog:** Typisk `/var/log/nginx/access.log` – hver request med statuskode, URI, IP.
- **Fejllog:** Typisk `/var/log/nginx/error.log` – fejl fra Nginx (fx "connection refused" til backend, fil ikke fundet).

Efter ændring: `sudo tail -f /var/log/nginx/error.log` mens I tester. Tjek også at konfigurationen er gyldig: `sudo nginx -t`.

---

## Typiske fejl

| Symptom | Mulig årsag | Tjek |
|---------|-------------|------|
| **502 Bad Gateway** | Nginx kan ikke nå backend (app på port 3000). | Er appen startet? Lytter den på 127.0.0.1:3000? Tjek error.log for "connection refused". |
| **404 Not Found** | Fil findes ikke eller `root`/`try_files` forkert. | Tjek at `root`-mappen og filer findes og at Nginx har læsetilladelse. |
| **403 Forbidden** | Nginx har ikke tilladelse til at læse filer. | `root`-mappen og filer skal være læsbare for Nginx-brugeren (typisk www-data). `chmod`/ejerskab. |
| **Certifikat "not trusted" / udløbet** | SSL-certifikat mangler eller er udløbet. | `sudo certbot renew --dry-run`. Tjek at Certbot-timer/cron kører. Se [[Lets-Encrypt-og-SSL]]. |
| **"Welcome to nginx" i stedet for jeres side** | Forkert server block matcher, eller jeres site er ikke i `sites-enabled`. | Tjek `server_name` og at der findes symlink i `sites-enabled`. `sudo nginx -T` viser aktiv konfiguration. |

---

## Nyttige kommandoer

- `sudo nginx -t` – test konfiguration.
- `sudo nginx -T` – vis hele den konfiguration Nginx bruger (inkl. inkluderede filer).
- `sudo systemctl status nginx` – er Nginx kørende?
- `sudo systemctl reload nginx` – genindlæs konfiguration uden nedetid.
