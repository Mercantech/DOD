---
tags:
  - dod
  - nginx-https
---

# Dag 4 – Web Server Setup (Nginx) + HTTPS & SSL

> Teori til Dag 4 (11. juni). Her får *jeres* app en rigtig webadresse med HTTPS – Nginx serverer indhold, og Let's Encrypt sikrer krypteret forbindelse. Se [[Program]] for dagens mål og plan. **Dybere pensum:** [[../../Nginx-og-HTTPS/00-Nginx-og-HTTPS-overblik]] (virtual hosts, reverse proxy, Let's Encrypt, fejlsøgning).

---

## Nginx – hvad og hvorfor

**Nginx** er en web server og reverse proxy: den modtager HTTP(S)-forespørgsler og kan servere statiske filer, videresende til en app (fx på port 3000) eller fungere som load balancer. Den er meget udbredt, hurtig og nem at konfigurere med **virtual hosts** (ét domæne/subdomain per konfiguration).

- **Installation (Linux):** `sudo apt update`, `sudo apt install nginx`. Start og aktiver: `sudo systemctl enable nginx`, `sudo systemctl start nginx`. Tjek med `curl http://localhost` eller åbn serverens IP i browseren – default "Welcome to nginx!" betyder at det virker.
- **Konfigurationsfiler:** Under `/etc/nginx/` – `nginx.conf` (hovedkonfiguration) og ofte `sites-available/` (tilgængelige sites) og `sites-enabled/` (symlinks til de aktive). Efter ændring: `sudo nginx -t` (test), `sudo systemctl reload nginx` (genindlæs uden nedetid).

---

## Virtual hosts og static file serving

En **virtual host** (server block) fortæller Nginx: "Når nogen beder om *dette* domæne eller denne server-navn, gør sådan her." I kan have én fil per projekt/subdomain.

**Eksempel – simpel static site:**

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

- `listen 80`: lyt på port 80 (HTTP).
- `server_name`: det domæne/subdomain denne blok gælder for (skal matche DNS).
- `root`: mappen hvor de statiske filer ligger (fx HTML, CSS, JS).
- `index index.html`: default fil ved forespørgsel til `/`.
- `try_files`: server filen hvis den findes, ellers 404.

**Praktisk:** Opret mappen (fx `sudo mkdir -p /var/www/jeresprojekt`), sæt en `index.html` med "Hello World" eller jeres indhold, og opret/aktiver konfigurationen i `sites-available` med symlink i `sites-enabled`. Så har I en "Hello World"-side klar – næste skridt er HTTPS.

---

## HTTPS og Let's Encrypt

**HTTPS** er HTTP krypteret med TLS/SSL: trafikken mellem browser og server kan ikke læses af andre. Browsere viser et lås-ikon og forventer i dag at rigtige sites bruger HTTPS.

**Let's Encrypt** udsteder gratis, betroede certifikater. De er gyldige i 90 dage og kan fornyes automatisk med **Certbot**.

- **Certbot:** Værktøjet der taler med Let's Encrypt, får et certifikat og (ofte) konfigurerer Nginx til at bruge det. Installér: `sudo apt install certbot python3-certbot-nginx`.
- **Krav:** Domænet skal pege på jeres server (DNS A-record), og port 80 skal være åben (Let's Encrypt bruger HTTP-challenge som standard). Nginx må køre, så Certbot kan sætte en valideringsfil eller bruge Nginx-plugin.

**Udsted certifikat (Nginx-plugin):**

```bash
sudo certbot --nginx -d jeresprojekt.mercantec.tech
```

Certbot opretter eller opdaterer en server block der lytter på 443 (HTTPS), sætter certifikatstier og genindlæser Nginx. I bliver spurgt om e-mail (til udløbsadvarsler) og om I vil redirecte HTTP → HTTPS (anbefales).

---

## Auto-fornyelse

Let's Encrypt-certifikater udløber efter 90 dage. **Certbot** opretter en cron-job eller systemd-timer der kører `certbot renew`. Tjek med:

```bash
sudo certbot renew --dry-run
```

Hvis det lykkes i dry-run, vil den rigtige fornyelse også virke. Sørg for at Nginx stadig lytter på 80 (for challenge) eller at DNS-01 bruges, så fornyelse kan gennemføres uden nedetid.

---

## HTTP → HTTPS redirect

Det er vigtigt at **al** trafik går over HTTPS, så ingen sender adgangskoder eller data u krypteret. I Nginx gør man typisk sådan:

- **Server block for port 80:** Kun én ting – redirect til HTTPS.

```nginx
server {
    listen 80;
    server_name jeresprojekt.mercantec.tech;
    return 301 https://$server_name$request_uri;
}
```

- **Server block for port 443:** Her ligger den egentlige konfiguration med `ssl_certificate` og `ssl_certificate_key` (Certbot sætter ofte disse selv). Alle forespørgsler til `http://...` rammer først port 80 og bliver sendt videre til `https://...`.

**Hvorfor det er vigtigt:** Uden redirect kan brugere ved et uheld bruge HTTP; trafikken er så ukrypteret og sårbar overfor lytning og session-hijacking. En konsekvent redirect sikrer at alle bruger HTTPS.

---

## Læringsmål (opsummering)

1. Installere og konfigurere Nginx til at servere statiske filer via en virtuel host.
2. Udstede og aktivere et Let's Encrypt-certifikat med auto-fornyelse (Certbot).
3. Tvinge HTTP-trafik over til HTTPS og forklare, hvorfor det er vigtigt.
