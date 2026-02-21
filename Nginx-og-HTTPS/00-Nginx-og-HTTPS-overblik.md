---
tags:
  - dod
  - nginx-https
---

# Nginx og HTTPS – pensum og overblik

Dette er **Nginx- og HTTPS-pensum** til DoD-kurset. Mappen bruges sammen med [[../Noter/DoD - Pensum/Program]] og dag-noterne. Her finder I dybdegående teori om **Nginx**, **virtual hosts**, **reverse proxy** og **Let's Encrypt** – mere end I når på Dag 4.

> **Vil I dybere end hvad I når på en enkelt dag?** Start i [[../Noter/DoD - Pensum/Dag-04-Nginx-og-HTTPS]]; brug denne mappe når I vil forstå konfiguration, proxy og SSL i detaljer.

---

## Indhold i denne mappe

| Note | Indhold | Relevant for |
|------|---------|--------------|
| **[[Nginx-grundlæggende]]** | Installation, konfigurationsstruktur, virtual hosts, static file serving | **Dag 4** |
| **[[Nginx-reverse-proxy]]** | Reverse proxy til app (fx port 3000), proxy_pass, headers, WebSocket | Dag 4, Dag 5 |
| **[[Lets-Encrypt-og-SSL]]** | Certbot, HTTP-01 challenge, auto-fornyelse, HTTP→HTTPS redirect, typiske fejl | **Dag 4** |
| **[[Fejlsøgning-Nginx]]** | Logs, 502/404, tilladelser, certifikat-problemer | Dag 4 |

---

## Sådan hænger det sammen med kurset

- **Uge 24, Dag 2:** DNS og firewall – DNS skal pege på jeres server før Nginx og Let's Encrypt virker. Se [[../DNS-og-Firewall/00-DNS-og-Firewall-overblik]].
- **Uge 24, Dag 4:** Nginx og HTTPS – brug [[Nginx-grundlæggende]], [[Nginx-reverse-proxy]], [[Lets-Encrypt-og-SSL]]. Dag-note: [[../Noter/DoD - Pensum/Dag-04-Nginx-og-HTTPS]].
- **Senere:** Dokploy kan sætte apps bag Nginx; reverse proxy-konceptet gælder stadig. Se [[../CICD/00-CICD-overblik]].

**Kort:** Dag 4 giver overblik; Nginx-og-HTTPS-mappen her giver **dybde** til dem der vil læse og fejlsøge videre.
