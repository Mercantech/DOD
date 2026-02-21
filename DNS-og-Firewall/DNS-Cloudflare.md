---
tags:
  - dod
  - dns-firewall
  - dns-firewall/dns
---

# DNS og Cloudflare

> **Dybere end dagens teori:** Flytte DNS til Cloudflare, proxy vs. DNS only, subdomains. Dag-note: [[../Noter/DoD - Pensum/Dag-02-Domæne-DNS-og-Firewall]]. DNS-records: [[DNS-grundlæggende]].

---

## Hvorfor flytte DNS til Cloudflare?

- **Ét sted til alle records:** A, CNAME, TXT osv. i et tydeligt dashboard.
- **Proxy og sikkerhed:** Trafik kan gå via Cloudflares netværk (DDoS-beskyttelse, caching, SSL mod besøgende).
- **Skjult server-IP:** Ved proxy ser angribere Cloudflares IP’er, ikke jeres egen server-IP.
- **Hurtig propagation:** Cloudflares DNS-netværk er globalt; ændringer spredes hurtigt.

---

## Sådan flytter man DNS til Cloudflare

1. **Tilføj domænet i Cloudflare** (Add site). Cloudflare kan scanne eksisterende records og foreslå dem.
2. **Cloudflare viser to nameservere**, fx `ada.ns.cloudflare.com` og `bob.ns.cloudflare.com`.
3. **Gå til din registrar** (fx Simply, GoDaddy) og find **Nameservers** / **DNS-servere** for domænet. Erstat de nuværende med de to Cloudflare angav.
4. **Gem hos registraren.** Nu håndterer Cloudflare DNS for domænet; alle records redigeres i Cloudflare.
5. **Vent på propagation** (ofte 15 min – 24 timer). Cloudflare viser typisk status (Active) når domænet bruger deres nameservers.

Efter flytningen opretter I **alle** DNS-records i Cloudflare. Subdomains til jeres projekter sættes som A- eller CNAME-records under det pågældende domæne.

---

## Proxy (orange sky) vs. DNS only (grå sky)

For hvert record kan I vælge:

| Tilstand | Betydning |
|----------|-----------|
| **Proxied (orange sky)** | Trafikken går gennem Cloudflare. DDoS-beskyttelse, caching, SSL mod besøgende; server-IP skjult. Cloudflare håndterer kryptering mod jeres server (origin). |
| **DNS only (grå sky)** | Kun DNS-opslag; trafikken går **direkte** til jeres server-IP. I håndterer SSL selv (fx Let's Encrypt på Nginx). |

**Praktisk:** Brug **Proxied** hvis I vil have Cloudflares beskyttelse og nem SSL. Brug **DNS only** hvis I selv kører Let's Encrypt på serveren og vil undgå at Cloudflare "sidder foran" (fx ved HTTP-01 challenge).

---

## Subdomains til jeres projekter

- Opret **A-record** med navn = subdomain (fx `jeresprojekt`) og værdi = jeres servers offentlige IP.
- Eller **CNAME** der peger på et andet host med A-record.
- Vælg Proxied eller DNS only som beskrevet ovenfor.

Se [[DNS-grundlæggende]] for TTL, propagation og fejlsøgning.
