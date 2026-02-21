---
tags:
  - dod
  - cicd
  - cicd/dokploy
---

# Dokploy – overblik

> **Dybere end dagens teori:** Hvad Dokploy er og hvordan det bruges i kurset. Dag-note: [[../Noter/DoD - Pensum/Dag-08-Dokploy-og-GitHub]]. Install og webhook: [[Dokploy-installation-og-setup]], [[Dokploy-GitHub-og-webhooks]].

---

## Hvad er Dokploy?

**Dokploy** er en **self-hosted PaaS** (Platform as a Service): I kører det på jeres egen server og bruger det til at deploye apps fra Git. I stedet for at logge ind på serveren og køre `docker build` og `docker compose up` manuelt ved hver ændring, forbinder I et GitHub-repository til Dokploy og – med en **webhook** – udløser et **push** automatisk byg og deploy.

- **I praksis:** Dokploy bygger jeres image (fra Dockerfile eller docker-compose), starter eller opdaterer containere, og kan håndtere **volumes** til database. Se [[Dokploy-build-og-deploy]] og [[Dokploy-volumes-og-monitoring]].
- **CI vs. CD:** I kurset håndteres **CI** (test ved PR/push) med GitHub Actions; **CD** (deployment) med **Dokploy**. Se [[CI-og-CD-koncepter]].

---

## Hvor passer Dokploy ind?

| Rolle | Værktøj |
|-------|---------|
| Teste kode før merge | GitHub Actions (CI) |
| Deploye efter push til main | Dokploy (CD) |

Et andet eksempel på automatiseret deployment er **[[../Noter/Proxi-demo]]**: Ansible-playbooks bygger image og deployer til K3s – samme idé, andet værktøj.

---

## Forudsætninger for Dokploy

- Server med **Docker** (og evt. Docker Compose).
- Adgang via **SSH** (evt. Twingate).
- **Domæne eller subdomæne** der peger på serveren (fx `dokploy.jeresdomæne.dk`) er nyttigt til web interface med HTTPS.

Næste skridt: [[Dokploy-installation-og-setup]].
