---
tags:
  - dod
  - nginx-https
  - nginx-https/ssl
---

# Let's Encrypt og SSL

> **Dybere end dagens teori:** Certbot, challenge, auto-fornyelse og HTTP→HTTPS. Dag-note: [[../Noter/DoD - Pensum/Dag-04-Nginx-og-HTTPS]]. Nginx: [[Nginx-grundlæggende]]. Fejlsøgning: [[Fejlsøgning-Nginx]].

---

## Hvorfor HTTPS?

**HTTPS** er HTTP krypteret med TLS/SSL: trafikken mellem browser og server kan ikke læses af andre. Browsere forventer HTTPS; mange APIs og sessions kræver det. **Let's Encrypt** udsteder gratis, betroede certifikater (gyldige 90 dage, fornyes med Certbot).

---

## Forudsætninger

- **DNS:** Domænet skal pege på jeres server (A- eller CNAME-record). Se [[../DNS-og-Firewall/DNS-grundlæggende]].
- **Port 80 åben:** Let's Encrypt bruger **HTTP-01 challenge** som standard – en request til `http://domæne/.well-known/acme-challenge/...` skal nå jeres server. Firewall skal tillade 80 ([[../DNS-og-Firewall/Firewall-UFW-iptables]]).
- **Nginx kørende:** Certbot med Nginx-plugin kan selv opdatere Nginx; alternativt kan I bruge **DNS-01** challenge (TXT-record) hvis HTTP ikke kan bruges.

---

## Certbot – udsted certifikat

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d jeresprojekt.mercantec.tech
```

Certbot opretter/opdaterer en server block på port 443 med `ssl_certificate` og `ssl_certificate_key`, og spørger om e-mail (udløbsadvarsler) og **redirect HTTP → HTTPS** (vælg Ja).

---

## Auto-fornyelse

Certbot opretter typisk en cron-job eller systemd-timer der kører `certbot renew`. Tjek med:

```bash
sudo certbot renew --dry-run
```

Sørg for at port 80 stadig er åben (for HTTP-01 ved fornyelse), eller brug DNS-01 hvis I kun eksponerer 443.

---

## HTTP → HTTPS redirect

Alle requests til HTTP skal sendes videre til HTTPS:

```nginx
server {
    listen 80;
    server_name jeresprojekt.mercantec.tech;
    return 301 https://$server_name$request_uri;
}
```

Server block på 443 indeholder den egentlige konfiguration med SSL. Uden redirect kan brugere ved uheld bruge HTTP – trafikken er så ukrypteret.

---

## Typiske Let's Encrypt-fejl

- **"Connection refused" / challenge fejler:** Tjek at DNS peger på serveren og at port 80 er åben. Tjek at Nginx kører og at `server_name` matcher domænet.
- **"Too many certificates":** Let's Encrypt har rate limits; vent eller brug staging (`--staging`) til test.
- **Certifikat udløbet:** Kør `sudo certbot renew`. Tjek at cron/timer kører og at `certbot renew --dry-run` lykkes.
