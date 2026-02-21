---
tags:
  - dod
  - cicd
  - cicd/dokploy
---

# Dag 8 – Dokploy Installation, Setup & GitHub Integration

> Teori til Dag 8 (17. juni). I dag sætter I **Dokploy** op på jeres server og kobler det til **GitHub**, så et push udløser automatisk deployment af *jeres* app. Se [[Program]] for dagens mål og plan. **Mere om CI/CD:** [[CICD og GitHubActions]]. **Dybere pensum:** [[../../CICD/00-CICD-overblik]] (Dokploy, webhooks, GitHub Actions). Volumes og data persistence dykkes i [[Dag-09-Volumes-Dokploy-og-Kubernetes]].

---

## Hvad er Dokploy?

**Dokploy** er en **self-hosted PaaS** (Platform as a Service): I kører det på jeres egen server og bruger det til at deploye apps fra Git. I stedet for at logge ind på serveren og køre `docker build` og `docker compose up` manuelt ved hver ændring, forbinder I et GitHub-repository til Dokploy og – med en **webhook** – udløser et **push** automatisk byg og deploy.

- **I praksis:** Dokploy bygger jeres image (fra Dockerfile eller docker-compose), starter eller opdaterer containere, og kan håndtere **volumes** til database, så data overlever genstart (volume mapping og backup kommer også på banen – [[Dag-09-Volumes-Dokploy-og-Kubernetes]]).
- **CI vs. CD:** I dette kursus håndteres **CI** (test ved PR/push) typisk med GitHub Actions; **CD** (deployment efter at koden er klar) håndteres af **Dokploy**. Se [[CICD og GitHubActions]] for hvordan det hænger sammen.

---

## Installere og konfigurere Dokploy på en server

### Forudsætninger

- En server med **Docker** (og evt. Docker Compose) installeret – som I har fra tidligere dage.
- Adgang via **SSH** og evt. **Twingate** efter kursets setup.
- En **domæne eller subdomæne** der peger på serveren (fx `dokploy.jeresdomæne.dk`) er nyttigt, så I kan åbne Dokploy’s web interface sikkert (HTTPS anbefales).

### Installationsskridt (kort)

1. **Installation** – Dokploy leveres typisk som en **Docker-baseret** install: I kloner Dokploy’s repo eller bruger deres install-script, der starter Dokploy som container(e) på serveren. Følg den aktuelle dokumentation fra [Dokploy](https://dokploy.com) eller underviserens anvisninger – kommandoer kan ændre sig mellem versioner.
2. **Første adgang** – Åbn Dokploy’s web interface (fx `https://dokploy.jeresdomæne.dk`). Opret admin-bruger og sikr at port/firewall tillader adgang (evt. bag Nginx med Let’s Encrypt som på Dag 4).
3. **Konfiguration** – I Dokploy konfigurerer I typisk:
   - **Server/agent:** Hvor skal apps deployes? (Ofte den samme maskine hvor Dokploy kører.)
   - **Build-metode:** Dockerfile, docker-compose eller andet – afhænger af jeres projekt.

Når Dokploy kører og I kan logge ind, er næste skridt at **forbinde et GitHub-repository**.

---

## Forbinde et GitHub-repository med Dokploy

1. **Opret et projekt/app i Dokploy** – Vælg "New Project" eller "New Application" og vælg typen (fx "Docker" eller "Docker Compose").
2. **Tilføj Git-kilde** – Angiv jeres GitHub-repository (URL eller `owner/repo`). Dokploy har brug for adgang til repo’et:
   - **Offentligt repo:** Ofte ingen ekstra konfiguration.
   - **Privat repo:** I skal give Dokploy adgang – typisk via **Personal Access Token (PAT)** eller **Deploy Key** (SSH). PAT oprettes under GitHub → Settings → Developer settings → Personal access tokens, med scope fx `repo`. Deploy Key er en SSH-nøgle I tilføjer under repo → Settings → Deploy keys.
3. **Vælg branch** – Fx `main` eller `master`, så Dokploy bygger og deployer fra den branch.
4. **Build-konfiguration** – Angiv hvor Dockerfile eller `docker-compose.yml` ligger (typisk rod af repo), og evt. build-argumenter eller environment variables som kun skal bruges på serveren (ikke i koden).

Dokploy kan nu **manuelt** bygge og deploye når I trykker "Deploy". For at gøre det **automatisk** ved hvert push, sætter I en **webhook** op.

---

## Opsætte webhook (GitHub → Dokploy)

En **webhook** er en HTTP-anmodning som GitHub sender til en URL (Dokploy’s) når der sker noget i repo’et – fx et push til `main`. Dokploy lytter på den URL og starter derefter byg + deploy.

### I Dokploy

- Under jeres app/projekt findes typisk en **"Webhook"**-sektion med en URL, fx:  
  `https://dokploy.jeresdomæne.dk/api/webhook/...` (med et hemmeligt token i URL’en).
- Kopiér den fulde webhook-URL – den skal ind i GitHub.

### I GitHub

1. Gå til jeres repository → **Settings** → **Webhooks** → **Add webhook**.
2. **Payload URL:** Indsæt Dokploy’s webhook-URL.
3. **Content type:** Ofte `application/json`.
4. **Trigger:** Vælg "Just the push event" (eller som anvist) så kun push – fx til `main` – udløser deployment.
5. **Secret (valgfrit):** Hvis Dokploy understøtter det, kan I sætte en fælles secret og verificere anmodninger. Ellers lad den tom efter anvisning.
6. Gem webhook. GitHub viser en flueben når den sidste delivery lykkedes.

Efter det vil et **push til den valgte branch** sende en request til Dokploy, som så bygger og deployer.

---

## Demonstrere at et Git push udløser automatisk deployment

For at **demonstrere** at det virker:

1. **Starttilstand** – Notér den nuværende version af jeres app (fx "Version 1" eller commit-hash). Åbn appen i browseren.
2. **Lav en lille ændring** – Fx en tekst i frontend eller en kommentar i kode. Commit og **push til `main`** (eller den branch I har knyttet til Dokploy).
3. **Observer** – I Dokploy’s interface bør I se at en ny **build/deploy** er startet (ofte med status "Building" eller "Deploying"). Vent til den er færdig.
4. **Verificer** – Genindlæs jeres app i browseren. Den skal vise den nye ændring – uden at I manuelt har kørt nogen kommandoer på serveren.

Så har I vist at **push → webhook → Dokploy → automatisk deployment** fungerer. Det er kernen i **CD** (Continuous Deployment) i jeres setup.

---

## Volume mapping og data persistence (kort)

Programmet nævner **volume mapping for database**, **data persistence** og **backup**. I Dokploy konfigurerer I typisk:

- **Volumes** til databasen (fx Postgres), så data ligger uden for den flygtige container og **overlever container restarts** og gen-deploys.
- **Backup-strategier** – fx regelmæssig dump af database til fil eller anden lagring – kan sættes op manuelt eller via scripts/Dokploy efter behov.

Disse emner dykkes dybere på **Dag 9** ([[Dag-09-Volumes-Dokploy-og-Kubernetes]]), hvor I også arbejder videre med Dokploy og får indblik i Kubernetes/k3s.

---

## Læringsmål (opsummering)

1. **Installere og konfigurere Dokploy på en server** – Docker-baseret install, adgang til web interface, grundlæggende konfiguration af server/build.
2. **Forbinde et GitHub-repository med Dokploy og opsætte webhook** – tilføje repo (evt. PAT eller Deploy Key ved privat repo), vælge branch, angive webhook-URL i GitHub så push udløser deploy.
3. **Demonstrere at et Git push udløser automatisk deployment** – lave en lille ændring, push til main, observere build i Dokploy og verificere at den nye version kører live.
