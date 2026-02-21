---
tags:
  - dod
  - cicd
  - cicd/dokploy
---

# Dag 10 – Monitoring & Logging med Dokploy

> Teori til Dag 10 (19. juni). I dag sætter I **monitoring og logging** op omkring *jeres* app – både via Dokploy’s egne funktioner og med et uptime-værktøj som **Uptime Kuma**, så I kan holde øje med at appen kører og hurtigt finde fejl. Se [[Program]] for dagens mål og plan. **Dybere pensum:** [[../../CICD/00-CICD-overblik]] (Dokploy logs, volumes, deployment-praksis). **Relateret:** [[Dag-14-Incident-Response]] (sikkerhedsmonitoring og incident response).

---

## Hvorfor monitoring og logging?

Når jeres app kører ude i produktion, skal I kunne:

- **Se om den kører** – er den oppe, svarer den på requests?
- **Finde fejl** – hvad skete der lige før et crash eller en fejl hos brugeren?
- **Reagere hurtigt** – hvis noget går ned, er det bedre at opdage det selv end at brugerne finder ud af det.

**Monitoring** = at overvåge status (CPU, hukommelse, er containeren kørende, svarer appen?).  
**Logging** = at læse de tekster (logs) som appen og containeren skriver ud – fejlbeskeder, requests, debug-info.

Uden logging og overvågning arbejder I "blind": I ved ikke om appen er nede, og I har svært ved at fejlsøge. Med simpel monitoring og adgang til logs får I **observability** – indsigt i hvad der sker i jeres løsning.

---

## Dokploy’s built-in monitoring

Dokploy giver typisk en oversigt over jeres projekter og apps direkte i web-interfacet. Det kan bruges som **grundlæggende monitoring**.

### Hvad kan I typisk se?

| Element | Beskrivelse |
|--------|-------------|
| **Container-status** | Om containeren kører (Running), er stoppet (Exited) eller fejler (Restarting/CrashLoop). |
| **Ressourcebrug** | CPU og hukommelse (RAM) for hver container – hjælper med at se om appen er overbelastet. |
| **Deploy-historik** | Seneste builds og deploys – hvornår blev den sidste version sat live, lykkedes den? |
| **Health / liveness** | Nogle setups viser om appen svarer på en bestemt URL (health check). |

### Hvor finder I det?

- **Projekt-/app-oversigten** – ofte en liste eller dashboard med alle jeres apps og deres status (grøn/rød, Running/Stopped).
- **Inde under en enkelt app** – detaljeret side med ressourcer, seneste deploy, og ofte **Logs** (se næste afsnit).

Aktiveringen er som regel **ingen ekstra konfiguration**: når I har deployet en app via Dokploy, er den med i oversigten. Hvis I ikke ser CPU/RAM, kan det afhænge af Dokploy-version og hvordan agenten er sat op – tjek underviserens anvisninger eller Dokploy’s dokumentation for jeres version.

---

## Application logging via Dokploy

**Logs** er den strøm af tekst som jeres app og container skriver til stdout/stderr – fx `console.log`, fejlbeskeder fra frameworket, eller Nginx/backend-logs. Dokploy samler typisk disse og viser dem i interfacet.

### Hvad vises i logs?

- **Build-logs** – output fra `docker build` og evt. install-trinn; nyttigt når et deploy fejler ved build.
- **Runtime-logs** – det jeres app skriver ud mens den kører: fejl, requests, warnings.
- **Container-logs** – hvad selve containeren (og evt. entrypoint-scripts) skriver.

I praksis: **runtime- og container-logs** er det I bruger mest til at fejlsøge en live app ("hvorfor crashede den?", "hvilken request gav 500?").

### Hvordan finder og bruger I logs i Dokploy?

1. Gå til jeres **projekt** og vælg den **app** I vil tjekke.
2. Find menupunktet eller fanen **"Logs"** (eller "Container logs" / "Application logs").
3. Vælg evt. hvilken container (hvis I har flere, fx app + database) – for fejl i selve appen vælger I app-containeren.
4. Logs vises ofte som **stream** (nye linjer kommer til nederst). Brug evt. scroll eller søg/filter hvis interfacet understøtter det.

**Tip:** Ved fejlsøgning, kig på de **sidste linjer** lige før en crash eller en fejl – ofte står fejlbeskeden der. Hvis jeres app ikke logger nok, kan I tilføje mere logging i koden (fx ved fejl) og redeploye.

---

## Uptime monitoring med Uptime Kuma

Ud over at se status i Dokploy kan I sætte **ekstern uptime monitoring** op: et værktøj der jævnligt tjekker om jeres app svarer (fx HTTP-request til jeres URL) og varsler hvis den er nede.

**Uptime Kuma** er et populært **self-hosted** værktøj: I kører det selv (fx i Docker på samme server eller anden maskine) og tilføjer "monitors" for jeres sider/API’er. Det kan sende notifikationer (email, Discord, Telegram osv.) når en tjeneste går ned eller kommer op igen.

*(I programmet står "UptimeKhana" – det kan være en lokal/alternativ betegnelse; konceptet er det samme: uptime-check fra et andet sted end Dokploy.)*

### Idéen med Uptime Kuma

- I opretter en **monitor** med jeres apps URL (fx `https://minapp.jeresdomæne.dk`).
- Uptime Kuma sender med jævne mellemrum en HTTP-request (heartbeat).
- Hvis svaret er OK (fx status 200), regnes tjenesten som **oppe**.
- Hvis den fejler eller ikke svarer inden for timeout, regnes den som **nede** – og I kan få en notifikation.

Det giver **uafhængig** overvågning: selv om Dokploy siger "Running", ved I nu om brugerne rent faktisk kan ramme appen (fx hvis Nginx er nede eller DNS fejler).

### Opsætning (kort)

1. **Kør Uptime Kuma** – fx med Docker: officielt image `louislam/uptime-kuma`. I kan køre det på samme server som Dokploy eller separat.
2. **Første gang** – åbn Uptime Kuma’s web interface, opret admin-bruger.
3. **Tilføj monitor** – vælg typen (HTTP(s)), indtast jeres apps URL, interval (fx hvert 60. sekund).
4. **Notifikationer (valgfrit)** – konfigurér en notifikationskanal (email, Discord, Telegram osv.), så I får besked når tjenesten går ned eller op igen.

Dokploy og Uptime Kuma **komplementerer** hinanden: Dokploy viser container-status og logs; Uptime Kuma viser om den **offentlige** URL faktisk svarer og kan sende alerts.

---

## Overblik: hvad bruger I hvornår?

| Behov | Hvor |
|-------|------|
| Er containeren startet? CPU/RAM? | Dokploy – app/projekt-oversigt og ressourcer |
| Hvad skrev appen lige før fejlen? | Dokploy – Logs for app-containeren |
| Svarer vores URL over for brugerne? | Uptime Kuma (eller tilsvarende uptime-værktøj) |
| Når noget går ned – hurtig besked | Uptime Kuma – notifikationer |

---

## Læringsmål (opsummering)

1. **Aktivere og bruge monitorering i Dokploy** – finde status på jeres apps (kørende/stopped), evt. CPU/RAM og deploy-historik, i Dokploy’s interface.
2. **Finde og forstå logs for jeres applikation i Dokploy** – åbne Logs for den relevante container, læse runtime-/container-logs og bruge dem til at fejlsøge (fx fejlbeskeder lige før et crash).
3. **Forklare hvorfor monitoring og logging er vigtigt i drift** – uden dem ved I ikke om appen kører, og I har svært ved at finde årsagen til fejl; med dem får I observability og mulighed for hurtig reaktion (især med uptime-alerts).

---

## Videre læsning

- **Dokploy:** [dokploy.com](https://dokploy.com) – officiel dokumentation til den version I bruger.
- **Uptime Kuma:** [github.com/louislam/uptime-kuma](https://github.com/louislam/uptime-kuma) – install, monitors og notifikationer.
- **Dag 14** ([[Dag-14-Incident-Response]]) – security monitoring, log analysis og incident response bygger videre på de samme idéer.
