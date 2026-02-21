---
tags:
  - dod
  - nginx-https
  - nginx-https/nginx
---

# Nginx – grundlæggende

> **Dybere end dagens teori:** Installation, konfigurationsstruktur og virtual hosts. Dag-note: [[../Noter/DoD - Pensum/Dag-04-Nginx-og-HTTPS]]. SSL: [[Lets-Encrypt-og-SSL]]. Reverse proxy: [[Nginx-reverse-proxy]].

---

## Hvad er Nginx?

**Nginx** er en web server og reverse proxy: den modtager HTTP(S)-forespørgsler og kan servere statiske filer, videresende til en app (fx på port 3000) eller fungere som load balancer. Meget udbredt, hurtig og nem at konfigurere med **virtual hosts** (server blocks) – ét domæne/subdomain per blok.

---

## Installation (Linux)

```bash
sudo apt update
sudo apt install nginx
sudo systemctl enable nginx
sudo systemctl start nginx
```

Tjek med `curl http://localhost` eller åbn serverens IP i browseren. "Welcome to nginx!" betyder at det virker.

---

## Konfigurationsstruktur

- **`/etc/nginx/nginx.conf`** – hovedkonfiguration; inkluderer ofte `sites-enabled/*`.
- **`/etc/nginx/sites-available/`** – tilgængelige site-filer (én per projekt/subdomain).
- **`/etc/nginx/sites-enabled/`** – symlinks til de aktive sites. Nginx læser kun det der er i `sites-enabled`.

**Efter ændring:** `sudo nginx -t` (test konfiguration), `sudo systemctl reload nginx` (genindlæs uden nedetid).

---

## Virtual host og static file serving

En **virtual host** (server block) fortæller Nginx: "Når nogen beder om *dette* domæne, gør sådan her."

```nginx
server {
    listen 80;
    server_name jeresprojekt.mercantec.tech;
    root /var/www/jeresprojekt;
    index index.html;
    location / {
        try_files $uri $uri/ =404;
    }
}
```

- **listen 80:** lyt på port 80 (HTTP).
- **server_name:** domæne/subdomain – skal matche DNS ([[../DNS-og-Firewall/DNS-grundlæggende]]).
- **root:** mappe med statiske filer (HTML, CSS, JS).
- **index index.html:** default fil ved `/`.
- **try_files:** server fil hvis den findes, ellers 404.

**Praktisk:** Opret mappen (`sudo mkdir -p /var/www/jeresprojekt`), sæt `index.html` med "Hello World", opret fil i `sites-available`, symlink til `sites-enabled`, reload Nginx.
