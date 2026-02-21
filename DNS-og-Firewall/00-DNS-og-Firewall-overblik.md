---
tags:
  - dod
  - dns-firewall
---

# DNS og Firewall – pensum og overblik

Dette er **DNS- og firewall-pensum** til DoD-kurset. Mappen bruges sammen med [[../Noter/DoD - Pensum/Program]] og dag-noterne. Her finder I dybdegående teori om **DNS**, **Cloudflare** og **firewall (UFW/iptables)** – mere end I når på Dag 2.

> **Vil I dybere end hvad I når på en enkelt dag?** Start i [[../Noter/DoD - Pensum/Dag-02-Domæne-DNS-og-Firewall]]; brug denne mappe når I vil forstå records, propagation, proxy og firewall-regler i detaljer.

---

## Indhold i denne mappe

| Note | Indhold | Relevant for |
|------|---------|--------------|
| **[[DNS-grundlæggende]]** | Domæner, DNS-records (A, CNAME, AAAA, TXT, NS), TTL, propagation, fejlsøgning med dig/nslookup | **Dag 2** |
| **[[DNS-Cloudflare]]** | Flytte DNS til Cloudflare, nameservers, proxy vs. DNS only, subdomains, SSL | **Dag 2** |
| **[[Firewall-UFW-iptables]]** | UFW kommandoer, port 22/80/443, default policies, iptables kort, typiske fejl og fejlsøgning | **Dag 2** |
| **[[NIS2-og-CRA]]** | Informationssikkerhed – NIS2 og CRA formål og anvendelse i virksomheden | Dag 2 (læringsmål 4) |

---

## Sådan hænger det sammen med kurset

- **Uge 24, Dag 2:** Domæne, DNS og Firewall – brug [[DNS-grundlæggende]], [[DNS-Cloudflare]], [[Firewall-UFW-iptables]]. Dag-note: [[../Noter/DoD - Pensum/Dag-02-Domæne-DNS-og-Firewall]].
- **Senere (Dag 4):** Nginx og HTTPS bygger på at DNS allerede peger på jeres server; Let's Encrypt bruger ofte DNS til verifikation. Se [[../Noter/DoD - Pensum/Dag-04-Nginx-og-HTTPS]].

**Kort:** Dag 2 giver overblik; DNS-og-Firewall-mappen her giver **dybde** til dem der vil læse og fejlsøge videre.
