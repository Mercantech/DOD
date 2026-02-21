---
tags:
  - dod
  - sikkerhed
---

# Dag 11 – OWASP Top 10 & moderne sikkerheds-headers

> Teori til Dag 11 (22. juni). I dag får *jeres* app et sikrere fundament – OWASP Top 10, sikkerheds-headers og sikkert input. Se [[Program]] for dagens mål og plan. **Dybere teori:** [[../../Sikkerhed/00-Sikkerhed-overblik]]. **Relateret:** [[Dag-10-Monitoring-og-Logging]] (A09 handler om logging/monitoring), [[Dag-12-Container-Security]] (sikre containere), [[Dag-13-CTF]] (praktisk brug af OWASP).

---

## OWASP Top 10 (2021)

**OWASP** (Open Web Application Security Project) vedligeholder en liste over de mest kritiske **sårbarheder** i webapplikationer. **Top 10** er den version, der bruges bredt til risikovurdering og undervisning. Her er 2021-udgaven med korte beskrivelser – I skal kunne **nævne og forklare flere** af dem.

| # | Sårbarhed | Kort forklaring |
|---|-----------|-----------------|
| **A01:2021 – Broken Access Control** | Brugere kan få adgang til data eller funktioner de ikke må. Fx manglende tjek af "er denne bruger ejer af denne ressource?", eller at API’er lækker data ved at gætte ID’er. |
| **A02:2021 – Cryptographic Failures** | Data der skal være hemmelige (passwords, tokens, PII) krypteres ikke, bruger svag kryptering, eller nøgler/credentials lækkes. |
| **A03:2021 – Injection** | Fjendtlig data sendes til fortolkeren (SQL, OS, LDAP, templating) og udføres som kode. **SQL injection** er den mest kendte: brugerinput sættes direkte ind i en query i stedet for parametriseret. |
| **A04:2021 – Insecure Design** | Manglende eller svag sikkerhedsdesign – fx ingen rate limiting, ingen modstand mod automatiserede angreb, eller for mange tillid til brugerinput. |
| **A05:2021 – Security Misconfiguration** | Standardpasswords, unødvendige features slået til, manglende sikkerheds-headers, fejlkonfigurerede CORS, eller verbose fejlmeddelelser der lækker info. |
| **A06:2021 – Vulnerable and Outdated Components** | Afhængigheder (biblioteker, frameworks) med kendte sårbarheder eller forældede versioner. Løsning: opdateringer og scanning (fx Dag 12 med Trivy/Snyk). |
| **A07:2021 – Identification and Authentication Failures** | Svage passwords, ingen 2FA, session-hijacking, eller credential stuffing. |
| **A08:2021 – Software and Data Integrity Failures** | Ukontrolleret integritet – fx at man ikke verificerer signaturer på opdateringer, eller at CI/CD-pipelines kan påvirkes (unsafe deserialization, supply chain). |
| **A09:2021 – Security Logging and Monitoring Failures** | Manglende eller utilstrækkelig logging af sikkerhedsrelevante hændelser, så angreb ikke opdages eller kan efterforskes. |
| **A10:2021 – Server-Side Request Forgery (SSRF)** | Appen laver HTTP-anmodninger baseret på brugerstyret URL. Angriberen kan få serveren til at kalde interne tjenester eller lække data. |

**Praktisk:** For *jeres* app er særligt **A01** (adgangskontrol), **A03** (injection – se nedenfor input), **A05** (misconfiguration – her kommer sikkerheds-headers ind) og **A06** (uddaterede komponenter) relevante at tænke på fra start.

---

## Moderne sikkerheds-headers

HTTP-**sikkerheds-headers** fortæller browseren hvordan siden må bruges og hvad der må loades – de **reducerer angrebsfladen** (fx XSS, clickjacking) og er en del af "secure by default". I kan sætte dem i **Nginx** (eller i jeres app hvis I sender response-headers selv).

### CSP (Content Security Policy)

**CSP** begrænser hvor indhold kan loades fra: scripts, styles, billeder, fonts, connections. Det begrænser **XSS** (Cross-Site Scripting), fordi selv om en angriber injicerer script, kan browseren blokere det hvis det ikke kommer fra en tilladt kilde.

**Eksempel (streng):**
```
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';
```

- `default-src 'self'` – kun ressourcer fra samme origin som siden.
- `script-src 'self'` – scripts kun fra egen origin (ingen inline uden nonce/hash).
- Efterhånden som I tilføjer CDN’er eller inline scripts, kan I udvide med konkrete domæner. Start restriktivt og slå kun det til I har brug for.

**Nginx:**  
`add_header Content-Security-Policy "default-src 'self'; ...";`

### HSTS (HTTP Strict Transport Security)

**HSTS** fortæller browseren: "Fremover skal dette site **kun** nås over HTTPS i en periode." Det mindsker risiko for downgrade-angreb og at brugere ved et uheld rammer HTTP.

**Eksempel:**
```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

- `max-age=31536000` – 1 år.
- `includeSubDomains` – gælder også subdomains.
- `preload` – kan indsendes til browseres preload-liste, så de aldrig prøver HTTP.  
Sæt kun HSTS når I er sikre på at HTTPS virker overalt (ellers kan brugere låses ude).

**Nginx:**  
`add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload";`

### X-Frame-Options

**X-Frame-Options** begrænser om siden må vises i en **iframe** – det beskytter mod **clickjacking** (en ond side indrammer jeres side og lokker brugeren til at klikke på skjulte elementer).

**Eksempel:**
```
X-Frame-Options: DENY
```
eller
```
X-Frame-Options: SAMEORIGIN
```

- `DENY` – må ikke indrammes.
- `SAMEORIGIN` – kun fra samme origin.

**Nginx:**  
`add_header X-Frame-Options "DENY";` eller `"SAMEORIGIN";`

### Andre nyttige headers

- **X-Content-Type-Options: nosniff** – browseren må ikke gætte content-type (reducerer risiko for MIME-type misbrug).
- **Referrer-Policy** – hvor meget af referrer-URL’en der sendes med (fx `strict-origin-when-cross-origin`).

**Nginx-eksempel (flere headers):**
```nginx
add_header X-Frame-Options "SAMEORIGIN";
add_header X-Content-Type-Options "nosniff";
add_header Referrer-Policy "strict-origin-when-cross-origin";
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload";
add_header Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';";
```

---

## Input validation og sanitization

**Usikker inputhåndtering** er bag mange sårbarheder: **injection** (A03), XSS, og fejl i forretningslogik. At **identificere** usikker håndtering og **undgå** det er et af dagens mål.

### Principper

- **Valider** input: type, format, længde og tilladte værdier (allowlist). Afvis eller returner fejl ved ugyldigt input – lad det ikke nå dybere ind i appen.
- **Brug aldrig brugerinput direkte som kode eller del af kommandoer.** Brug **parametriserede queries** (prepared statements) til SQL; brug sikre API’er til at bygge queries. Undgå at konkatenere brugerinput til SQL-streng.
- **Sanitizer/escape** output afhængigt af kontekst: HTML, JavaScript, URL, SQL. Så selv hvis noget farligt kommer ind, bliver det ikke udført som kode når det vises eller sendes videre.
- **Principle of least privilege:** Databasen og appen skal kun have de rettigheder der er nødvendige – begræns skadevirkningen ved et eventuelt break-in.

### Eksempler på usikker vs. sikker håndtering

**Usikker (SQL injection):**
```python
# BAD – aldrig gør sådan her
query = f"SELECT * FROM users WHERE id = {user_id}"
```
Angriber kan sætte `user_id = "1; DROP TABLE users;--"` eller læse andre rækker.

**Sikker (parametriseret):**
```python
# GOOD
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

**Usikker (XSS – output ikke escaped):**  
Hvis I viser brugerindtastet tekst direkte i HTML uden escape, kan angriber indsætte `<script>...</script>` og køre kode i andre brugere browsers.

**Sikker:**  
Brug framework’s escaping (fx React escaper automatisk; i server-renderet HTML brug funktioner der escape’r HTML-tegn) eller CSP til at begrænse hvor script kan køre fra.

### Kort checklist

- Alle brugerinputs valideres (type, format, range).
- SQL: kun parametriserede queries / prepared statements.
- Output til HTML/JS: escape i den rigtige kontekst (eller brug sikre API’er).
- Ingen hemmeligheder eller følsomme data i URL’er eller fejlmeddelelser.

---

## Læringsmål (opsummering)

1. Nævne og forklare flere af OWASP Top 10-sårbarhederne (2021) – fx A01, A03, A05, A06 som beskrevet ovenfor.
2. Implementere moderne sikkerheds-headers som CSP, HSTS og X-Frame-Options (evt. i Nginx eller i appen).
3. Identificere usikker inputhåndtering (fx direkte string til SQL, uescaped output) og forklare hvordan det kan undgås (parametrisering, validering, escaping).

---

## Videre læsning

- **Dag 10** ([[Dag-10-Monitoring-og-Logging]]) – A09: Security Logging and Monitoring Failures; logging understøtter opdagelse af angreb.
- **Dag 12** ([[Dag-12-Container-Security]]) – sikre containere og secrets.
- **Dag 13** ([[Dag-13-CTF]]) – praktisk CTF med OWASP-teknikker.
