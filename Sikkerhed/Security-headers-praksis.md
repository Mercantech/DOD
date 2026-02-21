---
tags:
  - dod
  - sikkerhed
  - sikkerhed/owasp
---

# Security headers – praksis

> **Dybere end dagens teori:** CSP, HSTS, X-Frame-Options i Nginx og app. Dag-note: [[../Noter/DoD - Pensum/Dag-11-OWASP-og-sikkerhed]]. Nginx: [[../Nginx-og-HTTPS/Nginx-grundlæggende]].

---

## Hvorfor sikkerheds-headers?

HTTP-**sikkerheds-headers** fortæller browseren hvordan siden må bruges og hvad der må loades. De reducerer angrebsfladen (XSS, clickjacking) og er en del af "secure by default". I kan sætte dem i **Nginx** (globalt for alle sites) eller i jeres **app** (response-headers).

---

## CSP (Content Security Policy)

**CSP** begrænser hvor indhold kan loades fra (scripts, styles, billeder). Begrænser **XSS** – selv injiceret script kan blokeres hvis det ikke kommer fra tilladt kilde.

**Eksempel (streng):**
```
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';
```

**Nginx:**  
`add_header Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';";`

Tilpas efter I tilføjer CDN eller inline scripts (evt. nonce eller hash). Start restriktivt.

---

## HSTS (HTTP Strict Transport Security)

**HSTS** fortæller browseren: "Dette site skal kun nås over HTTPS i en periode." Mindsker downgrade-angreb.

**Eksempel:**  
`Strict-Transport-Security: max-age=31536000; includeSubDomains; preload`

**Nginx:**  
`add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload";`

Sæt kun HSTS når HTTPS virker overalt – ellers kan brugere låses ude.

---

## X-Frame-Options

Beskytter mod **clickjacking** (ond side indrammer jeres side).  
`X-Frame-Options: DENY` eller `SAMEORIGIN`  
**Nginx:** `add_header X-Frame-Options "SAMEORIGIN";`

---

## Andre nyttige headers

- **X-Content-Type-Options: nosniff** – browseren må ikke gætte content-type.
- **Referrer-Policy: strict-origin-when-cross-origin** – begrænser hvad der sendes i Referer.

**Nginx-eksempel (alle):**
```nginx
add_header X-Frame-Options "SAMEORIGIN";
add_header X-Content-Type-Options "nosniff";
add_header Referrer-Policy "strict-origin-when-cross-origin";
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload";
add_header Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';";
```

Placer i den relevante `server { }`-blok (typisk for port 443).
