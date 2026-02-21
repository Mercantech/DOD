---
tags:
  - dod
  - sikkerhed
  - cicd
  - cicd/dokploy
---

# Dag 14 – Monitoring & Incident Response

> Teori til Dag 14 (25. juni). I dag kobler I **sikkerhed** på jeres monitoring og logging: hvordan I bruger Dokploy og logs til at opdage unormal aktivitet, og hvordan I planlægger reaktion på et **sikkerhedsbrud** (incident response). Der er også fokus på **risikovurdering** i konkrete hverdagssituationer (informationssikkerhed). Se [[Program]] for dagens mål og plan. **Dybere teori:** [[../../Sikkerhed/00-Sikkerhed-overblik]]. **Bygger på:** [[Dag-10-Monitoring-og-Logging]] (monitoring og logs i Dokploy).

---

## Security monitoring med Dokploy

På Dag 10 satte I **monitoring og logging** op – container-status, ressourcer og app-logs i Dokploy. På Dag 14 bruger I de samme værktøjer med **sikkerhedsbriller** på: hvad kan indikere et angreb, misbrug eller en konfigurationsfejl der udvider angrebsfladen?

### Hvad er sikkerhedsrelevant at overvåge?

| Observation | Hvor (typisk) | Hvorfor det kan betyde noget |
|-------------|----------------|-----------------------------|
| **Uventet høj CPU/RAM** | Dokploy – ressourcer | Kan indikere misbrug (fx crypto-mining), DDoS-effekt eller en løkke i koden. |
| **Container genstarter igen og igen** | Dokploy – status / deploy | CrashLoop kan skyldes angreb (fx minering) eller udnyttelse der crasher processen. |
| **Mange fejl i logs på kort tid** | Dokploy – Logs | 401/403, SQL-fejl eller stack traces kan vise forsøg på injection, brute force eller scanning. |
| **Ukendte IP’er eller mønstre** | Logs (access logs, app-logs) | Scanning, bot-trafik eller angreb fra bestemte kilder. |
| **Ændringer i deploy uden jeres push** | Dokploy – deploy-historik | Kun relevant hvis andre har adgang; kan indikere kompromitteret Git eller CI/CD. |

Dokploy giver ikke "sikkerhedsmonitoring" som et separat modul – I bruger **de samme** status- og log-visninger, men **tolker** dem med sikkerhed i baghovedet og reagerer ved mistanke (se nedenfor: log analysis og incident response).

---

## Log analysis og alerting

**Log analysis** = at læse og fortolke logs for at opdage **unormal aktivitet** eller **fejl** der kan være sikkerhedsrelevante.

### Hvad kan "unormal aktivitet" være?

- **Mange 404’s** fra samme IP – scanning efter sårbare filer eller endpoints.
- **Mange 401/403** – forsøg på at få adgang uden at være logget ind eller uden rettigheder.
- **Fejl i database-lag** – fx SQL-fejl med brugerinput i – kan tyde på **injection-forsøg**.
- **Strange User-Agent eller paths** – automatiseret skannerværktøjer, bots.
- **Pludselig stigning i trafik** – kan være legitim trafik eller DDoS/abuse.

I **Dokploy** åbner I som på Dag 10 **Logs** for den relevante container og kigger efter mønstre: gentagne fejl, IP’er der dukker mange gange op, eller beskeder I ikke kender. Hvis jeres app logger sikkerhedsrelevante hændelser (fx mislykkede logins), giver det endnu bedre mulighed for analyse.

### Alerting

**Alerting** betyder at få **besked** når noget sker – fx når en tjeneste går ned (som med Uptime Kuma på Dag 10) eller når en regel bliver overtrådt (fx "mere end X fejl per minut").  

I Dokploy er det typisk **deploy-status** og evt. **container ned** der kan give synlige advarsler. Mere avanceret alerting (fx ved bestemte log-mønstre) kræver ofte ekstra værktøjer (log-aggregation, regler og notifikationer). For jeres niveau er det vigtigt at **forstå idéen**: at kombinere monitoring + logs + evt. alerts gør det muligt at **opdage** en incident hurtigere og derefter reagere efter en plan.

---

## Hvad er en incident response plan?

En **incident response plan** (IRP) er en **forud aftalt plan** for hvordan organisationen (eller I som gruppe) reagerer, når en **sikkerhedsbegivenhed** eller et **sikkerhedsbrud** opdages – fx at jeres app er hacket, at data er lækket, eller at en tjeneste er nede på grund af angreb.

### Hvorfor er det vigtigt?

Uden en plan reagerer man ofte **ad hoc**: folk ved ikke hvem der skal gøre hvad, hvem der skal kontaktes, eller hvad der skal dokumenteres. Det kan forsinke inddæmning og gøre skaden større. Med en simpel plan har I:

- **Fælles forståelse** af hvad en "incident" er og hvornår planen træder i kraft.
- **Klare skridt** – hvem gør hvad, hvem informeres (brugerne, skolen, evt. myndigheder).
- **Dokumentation** – hvad skete, hvornår, hvad blev gjort – vigtigt for læring og evt. krav (fx NIS2/CRA om incident reporting).

---

## Faser i incident response (simpel model)

En klassisk model deler håndteringen i faser. I kan bruge denne som skabelon til jeres **simple plan**:

| Fase | Kort indhold |
|------|--------------|
| **1. Detect (opdag)** | Opdage at noget er galt – via monitoring, logs, brugerrapporter eller alerts. |
| **2. Contain (inddæm)** | Begrænse skaden: stop en kompromitteret service, luk et hul, bloker en IP, eller skift credentials. |
| **3. Eradicate (udryd)** | Fjerne årsagen: patch sårbarhed, fjern malware, ret fejlkonfiguration. |
| **4. Recover (genopret)** | Få systemet sikkert i drift igen: genstart, genopbyg, verificer at angrebet ikke gentager sig. |
| **5. Post-incident** | Dokumenter hvad der skete og hvad I lærte; opdater planen og sikkerhedstiltag. |

I jeres projekt behøver I ikke en lang juridisk tekst – en **kort liste** med: "Hvem kontakter vi? Hvad gør vi først (fx tjek logs, stop container, skift password)? Hvor noterer vi hvad der skete?" er allerede en **simpel incident response plan**.

---

## Opstille en simpel plan for jeres gruppe

For at opfylde læringsmålet om at **opstille en simpel plan** kan I lave noget i denne stil:

1. **Definition:** Hvad tæller som incident hos jer? (fx: appen er nede, mistanke om uautoriseret adgang, synlige fejl der lækker data.)
2. **Opdagelse:** Hvor kigger I? (Dokploy status og Logs, Uptime Kuma, brugerhenvendelser.)
3. **Første skridt:** Hvem gør hvad inden for gruppen? (fx: én tjekker logs, én kan stoppe/redeploy containeren, én noterer tidslinje.)
4. **Inddæmning:** Hvad gør I med det samme? (fx: stop app, skift adgangskoder, luk firewall til en IP.)
5. **Dokumentation:** Hvor gemmer I noter om hvad der skete og hvad I gjorde? (fx en fil i repo eller et delt dokument.)
6. **Efterfølgende:** Hvordan følger I op? (ret sårbarhed, opdater dependencies, gennemgå planen.)

Den konkrete indhold vil afhænge af jeres app og ressourcer – vigtigt er at I **har** en fælles, kort plan og ikke kun improviserer den dag noget går galt.

---

## Informationssikkerhed: Risikovurdering i konkrete hverdagssituationer

Dagens **informationssikkerhed**-element handler om at **indtænke risikovurdering** i løsningen af **konkrete hverdagssituationer**. Det betyder at I – på et grundlæggende niveau – kan:

- **Tænke risiko** – hvad kan der gå galt (datatab, uautoriseret adgang, nedetid), og hvad er konsekvensen?
- **Vurdere** – er chancen for at det sker lille eller stor? Er konsekvensen acceptabel eller alvorlig?
- **Beslute** – hvilke tiltag er fornuftige i forhold til risikoen? (fx: backup, adgangskontrol, monitoring, incident plan.)

**Eksempler på hverdagssituationer** (som I kan bruge til diskussion eller opgaver):

- En bruger vil gerne have adgang til et delt dokument – hvem skal have adgang, og hvad hvis linket lækker?
- I deployer en ny feature sent om aftenen – hvad hvis den bryder noget? Har I rollback eller en plan?
- I får en mail der beder om at "verificere jeres GitHub-login" – hvad er risikoen, og hvad bør I gøre?
- Logs viser mange fejlede login-forsøg fra én IP – er det en incident? Hvad gør I?

Risikovurdering behøver ikke være en stor rapport – det er **tænkning** over "hvad kan gå galt, og hvad gør vi så?" i de situationer I møder i projekter og i skolehverdagen. Det hænger sammen med incident response: når I har en plan og tænker risiko, reagerer I mere bevidst og struktureret.

---

## Læringsmål (opsummering)

1. **Bruge logs og monitorering til at opdage unormal aktivitet eller fejl** – i Dokploy: kigge på status, ressourcer og Logs med sikkerhed i baghovedet; genkende mønstre der kan tyde på angreb, misbrug eller fejl (fx mange 4xx/5xx, ukendte IP’er, crash loops).
2. **Forklare hvad en incident response plan er og hvorfor den er vigtig** – en forud aftalt plan for hvordan I reagerer ved et sikkerhedsbrud; den giver hurtigere og mere koordineret håndtering og bedre dokumentation.
3. **Opstille en simpel plan for reaktion på et sikkerhedsbrud** – fx med faserne detect → contain → eradicate → recover → post-incident, og konkrete afklaringer: hvem gør hvad, hvor I kigger (Dokploy, logs, alerts), og hvor I dokumenterer.
4. **På grundlæggende niveau indtænke risikovurdering i konkrete hverdagssituationer** – tænke "hvad kan gå galt, hvad er konsekvensen, og hvilke tiltag er fornuftige?" i situationer som delt adgang, deployment, phishing eller mistænkelig aktivitet i logs.

---

## Videre læsning

- **Dag 10** ([[Dag-10-Monitoring-og-Logging]]) – grundlag for monitoring og logs i Dokploy.
- **OWASP A09:2021 – Security Logging and Monitoring Failures** – i [[Dag-11-OWASP-og-sikkerhed]]; understreger vigtigheden af at logge sikkerhedsrelevante hændelser.
- **NIS2 / CRA** – lovkrav om incident reporting i visse sektorer; [[Dag-02-Domæne-DNS-og-Firewall]] nævner NIS2/CRA i informationssikkerheds-sammenhæng.
- **SANS / NIST** – incident response frameworks (mere avancerede modeller, hvis I vil udbygge jeres plan senere).
