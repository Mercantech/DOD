---
tags:
  - dod
  - sikkerhed
  - sikkerhed/ctf
---

# CTF og etik

> **Dybere end dagens teori:** CTF i kurset og etiske principper. Dag-note: [[../Noter/DoD - Pensum/Dag-13-CTF]]. OWASP: [[OWASP-Top-10-dybde]].

---

## Hvad er en CTF i dette kursus?

En **CTF** (Capture The Flag) er en øvelse hvor I finder og udnytter **sårbarheder** i en applikation for at nå bestemte mål (fx læse skjult data, få admin-adgang). I kurset gør I det i en **kontrolleret, etisk** ramme: på en app sat op til formålet, med tilladelse og uden at skade rigtige brugere eller systemer.

**Målet:** Opleve hvordan OWASP-sårbarheder ser ud i praksis og lære at **dokumentere** hvad I fandt og hvordan I udnyttede det.

---

## Teknikker fra OWASP

Under CTF’en bruger I fx:

- **A01 – Broken Access Control:** Få adgang til andre brugeres data ved at ændre ID’er i URL/API?
- **A03 – Injection:** SQL injection, command injection via inputfelter?
- **A05 – Security Misconfiguration:** Åbne debug-endpoints, standardpasswords, manglende headers?
- **A07 – Authentication Failures:** Svage passwords, ingen rate limiting?

Identificer sårbarheder systematisk (requests, inputs, fejlmeddelelser) og udnyt dem inden for øvelsens regler.

---

## Dokumentation af fund

- **Hvad** I fandt (fx "Login accepterer `' OR '1'='1`").
- **Hvorfor** det er en sårbarhed (fx SQL injection).
- **Hvordan** I udnyttede det (trin for trin).
- **Hvordan** det kunne rettes (parametriserede queries, validering).

---

## Etiske principper

- **Kun** teste systemer I har **tilladelse** til at teste (her: CTF-appen).
- **Ikke** udnytte sårbarheder til at skade andre eller stjæle data uden aftale.
- **Anvende** viden til at forbedre sikkerhed – fx undgå de samme fejl i egen kode.
- **Samarbejde** målrettet og etisk; hold jer til øvelsens rammer.
