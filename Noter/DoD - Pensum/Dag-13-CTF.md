---
tags:
  - dod
  - sikkerhed
---

# Dag 13 – CTF Challenge: "Hack en app"

> Teori til Dag 13 (24. juni). I dag tester I sikkerheden **praktisk** gennem en CTF (Capture The Flag) – I bruger teknikker fra OWASP til at finde og udnytte sårbarheder i en applikation, **etisk og målrettet**, og dokumenterer jeres fund. **Informationssikkerhed:** Etiske principper i arbejdet med data- og it-sikkerhed. Se [[Program]] for dagens mål og plan. **Dybere teori:** [[../../Sikkerhed/00-Sikkerhed-overblik]]. **Bygger på:** [[Dag-11-OWASP-og-sikkerhed]] (OWASP Top 10, input, headers) og evt. [[Dag-12-Container-Security]] (sikre containere).

---

## Hvad er en CTF i dette kursus?

En **CTF** (Capture The Flag) er en øvelse hvor I skal finde og udnytte **sårbarheder** i en applikation for at nå bestemte mål (fx at læse skjult data, få admin-adgang eller "stjæle" en flag). I kurset gør I det i en **kontrolleret, etisk** ramme: på en app der er sat op til formålet, med tilladelse og uden at skade rigtige brugere eller systemer.

**Målet** er at I oplever hvordan sårbarheder fra OWASP Top 10 ser ud i praksis – fx injection, broken access control eller usikker inputhåndtering – og at I lærer at **dokumentere** og **forklare** hvad I fandt og hvordan I udnyttede det.

---

## Teknikker fra OWASP – hvad kan I bruge?

Fra **Dag 11** ([[Dag-11-OWASP-og-sikkerhed]]) kender I fx:

- **A01 – Broken Access Control:** Kan I få adgang til andre brugeres data ved at ændre ID’er i URL eller API?
- **A03 – Injection:** SQL injection, command injection eller anden indsprøjtning af kode via inputfelter?
- **A05 – Security Misconfiguration:** Åbne debug-endpoints, standardpasswords, manglende sikkerheds-headers?
- **A07 – Identification and Authentication Failures:** Svage passwords, ingen rate limiting på login, session-håndtering?

Under CTF’en prøver I systematisk at **identificere** sådanne sårbarheder (fx ved at inspicere requests, prøve forskellige inputs, læse fejlmeddelelser) og **udnytte** dem for at nå øvelsens mål – altid inden for de regler underviser eller opgaven sætter.

---

## Dokumentation og forklaring

Læringsmålene kræver at I kan **dokumentere og forklare** hvordan en sikkerhedsbrist blev udnyttet. Det betyder typisk:

- **Hvad** I fandt (fx "Login accepterer enhver brugernavn med password `' OR '1'='1`").
- **Hvorfor** det er en sårbarhed (fx SQL injection fordi brugerinput sættes direkte ind i en query).
- **Hvordan** I udnyttede det (trin for trin: hvilken request, hvilket svar, hvad I fik adgang til).
- **Hvordan** det kunne rettes (fx parametriserede queries, inputvalidering).

Den slags noter eller kort rapport gør det nemmere at fremlægge for gruppen og at reflektere over etik (næste afsnit).

---

## Etiske principper i arbejdet med data- og it-sikkerhed

**Informationssikkerhed** på dag 13 inkluderer at I kan **redegøre for etiske principper** i arbejdet med data- og it-sikkerhed. Det handler om at:

- **Kun** teste og angribe systemer I har **tilladelse** til at teste (her: den CTF-app der er sat op til øvelsen).
- **Ikke** udnytte sårbarheder til at skade andre, stjæle data eller forstyrre drift uden aftale.
- **Anvende** jeres viden til at forstå og **forbedre** sikkerhed – fx ved at rapportere fund til ejeren af et system (i rigtige situationer) eller ved at undgå de samme fejl i jeres egen kode.
- **Samarbejde** målrettet og etisk i gruppen – fx at dele indsigt uden at eskalere angreb ud over øvelsens rammer.

I praksis: under CTF’en holder I jer til de regler og den app der er givet; I bruger teknikkerne til **læring** og **dokumentation**, ikke til uautoriseret indtrængen andre steder.

---

## Læringsmål (opsummering)

1. **Bruge teknikker fra OWASP til at identificere sårbarheder** – fx adgangskontrol, injection, misconfiguration eller svag autentifikation, som beskrevet på Dag 11.
2. **Dokumentere og forklare hvordan en sikkerhedsbrist blev udnyttet** – hvad I fandt, hvorfor det er en sårbarhed, hvordan I udnyttede det, og hvordan det kunne rettes.
3. **Samarbejde i en gruppe om at analysere og angribe en applikation etisk og målrettet** – inden for øvelsens rammer og uden at skade andre.
4. **Redegøre for etiske principper** i arbejdet med data- og it-sikkerhed – tilladelse, ansvar og brug af viden til at forbedre sikkerhed.

---

## Videre læsning

- **Dag 11** ([[Dag-11-OWASP-og-sikkerhed]]) – OWASP Top 10, sikkerheds-headers og input.
- **Dag 12** ([[Dag-12-Container-Security]]) – sikre containere og secrets (relevant for den app I angriber, hvis den kører i container).
- **Dag 14** ([[Dag-14-Incident-Response]]) – hvordan man opdager og reagerer på sikkerhedsbegivenheder; CTF giver indsigt i hvad man leder efter i logs og monitoring.
