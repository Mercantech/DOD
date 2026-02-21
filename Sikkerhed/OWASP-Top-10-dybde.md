---
tags:
  - dod
  - sikkerhed
  - sikkerhed/owasp
---

# OWASP Top 10 – dybde

> **Dybere end dagens teori:** Alle 10 (2021) med korte forklaringer og hvad I bør fokusere på. Dag-note: [[../Noter/DoD - Pensum/Dag-11-OWASP-og-sikkerhed]]. Headers: [[Security-headers-praksis]]. CTF: [[CTF-og-etik]].

---

## OWASP Top 10 (2021) – oversigt

| # | Sårbarhed | Kort forklaring |
|---|-----------|-----------------|
| **A01** | Broken Access Control | Brugere får adgang til data/funktioner de ikke må. Manglende tjek "er brugeren ejer?", API lækker ved at gætte ID'er. |
| **A02** | Cryptographic Failures | Hemmelige data krypteres ikke eller med svag kryptering; nøgler/credentials lækkes. |
| **A03** | Injection | Brugerinput sendes til fortolker (SQL, OS, templating) og udføres som kode. SQL injection: input direkte i query i stedet for parametriseret. |
| **A04** | Insecure Design | Manglende sikkerhedsdesign – ingen rate limiting, for meget tillid til brugerinput. |
| **A05** | Security Misconfiguration | Standardpasswords, manglende sikkerheds-headers, fejlkonfigureret CORS, verbose fejl der lækker info. |
| **A06** | Vulnerable and Outdated Components | Afhængigheder med kendte sårbarheder. Løsning: opdateringer og scanning (Trivy/Snyk). Se [[Container-sikkerhed]]. |
| **A07** | Identification and Authentication Failures | Svage passwords, ingen 2FA, session-hijacking, credential stuffing. |
| **A08** | Software and Data Integrity Failures | Ukontrolleret integritet – signaturer ikke verificeret, CI/CD kan påvirkes (supply chain). |
| **A09** | Security Logging and Monitoring Failures | Manglende logging af sikkerhedsrelevante hændelser – angreb opdages ikke. Se [[../Noter/DoD - Pensum/Dag-10-Monitoring-og-Logging]]. |
| **A10** | SSRF | Appen laver HTTP-requests baseret på brugerstyret URL; angriber kan få serveren til at kalde interne tjenester. |

---

## Hvad bør I fokusere på først?

For *jeres* app er særligt relevante:

- **A01 (Access Control):** Tjek altid "må denne bruger se/gøre dette?" før I returnerer data eller udfører handlinger.
- **A03 (Injection):** Brug **parametriserede queries** til SQL; valider og escape input. Se input-sektionen i Dag 11.
- **A05 (Misconfiguration):** Implementer sikkerheds-headers (CSP, HSTS, X-Frame-Options). Se [[Security-headers-praksis]].
- **A06 (Outdated Components):** Scan images med Trivy/Snyk; hold base og dependencies opdateret. Se [[Container-sikkerhed]].

A09 (logging) understøttes af monitoring på Dag 10 og 14; A02, A04, A07, A08, A10 kan I dykke ned i efter behov.
