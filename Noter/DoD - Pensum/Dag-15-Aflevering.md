---
tags:
  - dod
  - cicd
---

# Dag 15 – Aflevering/fremlæggelse

> Dag 15 (26. juni). Ingen teori – dagen bruges på aflevering eller fremlæggelse af deployment-projektet. Se [[Program]] for overblik og samme afleveringskrav. **Relateret:** [[Dag-14-Incident-Response]] (monitoring og incident response er en del af afleveringskrav om drift).

---

## Dagens læringsmål

1. Jeg kan samle og præsentere dokumentation for hele projektets infrastruktur og drift
2. Jeg kan forklare vores vigtigste tekniske beslutninger og reflektere over dem
3. Jeg kan præsentere vores løsning klart, teknisk og relevant – både det der virkede og det der ikke gjorde

---

## Aflevering – Deployment Projekt

### Formål

I har i grupper arbejdet med at deploye et projekt til en rigtig server med fokus på infrastruktur, sikkerhed, CI/CD og drift. Afleveringen handler ikke kun om at vise, hvad I *fik til at virke* – men også om, hvad I lærte undervejs.

---

### Indholdskrav (uanset format)

Alle grupper skal besvare de samme spørgsmål – *uanset* om I afleverer som rapport, video eller fremlæggelse:

1. **Projektbeskrivelse:**
   - Hvad har I forsøgt at bygge/deploye?
   - Hvilken tech stack brugte I?
2. **Infrastruktur og Deployment:**
   - Hvordan er det sat op? (Server, domæne, HTTPS, etc.)
   - Brugte I Docker, Nginx, database?
3. **CI/CD Pipeline:**
   - Hvordan deployer I? (Dokploy, GitHub Actions, manuelt)
   - Brug af versionstyring, branches, automatisering?
   - Indblik i projekt-styring med DevOps, GH-Projects eller lign.
4. **Sikkerhed:**
   - Hvilke tiltag tog I? (SSH, firewall, SSL, OWASP, secrets)
5. **Monitoring og Drift:**
   - Hvordan holder I øje med at jeres løsning kører?
   - Brug af logs, uptime-tools, fejlhåndtering?
6. **Læring og Refleksion:**
   - Hvad gik godt? Hvad gik skævt?
   - Hvad har I lært – teknisk og samarbejdsmæssigt?

---

### Afleveringsformater (vælg én)

#### 1. Rapport (PDF / Google Docs)

En skriftlig beskrivelse af jeres projekt og process, max 6 sider (ekskl. billeder). Altså 14.400 tegn med mellemrum. Opgaven her minder mest om en produktrapport til jeres svendeprøve, så det kan være god træning til den tid!

**Krav:**
- Strukturér rapporten efter de 6 punkter
- Gerne med screenshots, shell output, GitHub links osv.

📥 **Afleveres via Teams som en PDF**  
🕓 **Deadline**: 26. juni kl. 23:59

---

#### 2. Videoaflevering (max 10 minutter)

En kort screencast hvor I **viser og forklarer** jeres løsning og hvordan den fungerer. Ingen krav om webcam – kun lyd og skærm er fint. Alle gruppe medlemmer skal være med og sige noget af projektet. Om I sidder i et opkald og optager eller tager final-cut ud og klipper sammen er op til jer, men det skal sendes som en fil!

**Krav:**
- Følg de 6 punkter mundtligt
- Vis jeres opsætning, GitHub repo, terminal, app m.m.
- Hold det konkret og fokuseret

📥 **Sendes på teams som en MP4**  
🕓 **Deadline**: 26. juni kl. 23:59

---

#### 3. Mundtlig fremlæggelse (grupper)

I fremlægger jeres projekt **live** online på 10 minutter + 5 min spørgsmål. Fremlæggelsen er som standard åben for alle, men ved særlige årsager kan det godt gøres kun med underviser og gruppen!

**Krav:**
- Kort præsentation efter de 6 punkter
- Vis evt. dele af jeres løsning (demo, repo, terminal)
- Alle i gruppen skal være med og alle siger noget

📥 **Tilmeld jer en tid via skema (kommer i uge 25)**  
🕓 **Afvikles: 26. juni**

---

### Vurderingskriterier

Det handler ikke om hvor "færdigt" det hele er, men om:

- Forståelse af **infrastruktur og deployment**
- Refleksion over **valg, fejl og løsninger**
- Evne til at **dokumentere og forklare** tekniske processer
