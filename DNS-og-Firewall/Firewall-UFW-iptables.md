---
tags:
  - dod
  - dns-firewall
  - dns-firewall/firewall
---

# Firewall – UFW og iptables

> **Dybere end dagens teori:** UFW kommandoer, typiske regler og fejlsøgning. Dag-note: [[../Noter/DoD - Pensum/Dag-02-Domæne-DNS-og-Firewall]].

---

## Hvad er en firewall?

En **firewall** styrer hvilke indgående og udgående forbindelser der må passere. På Linux bruges **iptables** (eller nftables) under hooden. **UFW** (Uncomplicated Firewall) er et enklere lag ovenpå, så I arbejder med "tillad SSH", "tillad HTTP/HTTPS" i stedet for rå iptables-regler.

---

## UFW – grundlæggende kommandoer

| Kommando | Betydning |
|----------|-----------|
| `sudo ufw allow 22/tcp` eller `sudo ufw allow ssh` | Tillad SSH (vigtigt **før** I aktiverer firewall). |
| `sudo ufw allow 80/tcp` | Tillad HTTP. |
| `sudo ufw allow 443/tcp` | Tillad HTTPS. |
| `sudo ufw default deny incoming` | Default: nægt alle indgående. |
| `sudo ufw default allow outgoing` | Default: tillad udgående. |
| `sudo ufw enable` | Aktiver firewall. |
| `sudo ufw status` eller `sudo ufw status verbose` | Se regler og status. |
| `sudo ufw delete allow 80/tcp` | Fjern en regel. |

**Vigtigt:** Tillad **SSH (22)** før I kører `ufw enable`. Ellers kan I låse jer selv ude.

---

## Typisk rækkefølge ved opsætning

1. `sudo ufw allow 22/tcp`
2. `sudo ufw allow 80/tcp`
3. `sudo ufw allow 443/tcp`
4. `sudo ufw default deny incoming`
5. `sudo ufw default allow outgoing`
6. `sudo ufw enable`

Derefter accepterer serveren kun indgående på 22, 80 og 443 (plus evt. andre I eksplicit tillader).

---

## Typiske fejl og fejlsøgning

- **"Jeg kan ikke SSH ind":** Har I tilladt 22 før enable? Tjek `sudo ufw status`. Evt. midlertidigt `sudo ufw disable` og ret reglerne (pas på hvis serveren er åben andre steder).
- **"Hjemmesiden loader ikke":** Er 80 og 443 tilladt? Er Nginx/app kørende? Tjek også at DNS peger på serverens IP ([[DNS-grundlæggende]]).
- **Dokploy eller anden service på anden port:** Tillad den port eksplicit, fx `sudo ufw allow 3000/tcp` (eller den port I bruger).

---

## iptables (kort)

**iptables** er den tekniske grundlag: regler baseret på port, protokol, kilde-IP osv. UFW skriver i praksis iptables-regler for dig. På nye systemer kan **nftables** være underlaget; konceptet er det samme. Til daglig brug er UFW nok.
