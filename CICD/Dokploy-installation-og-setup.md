---
tags:
  - dod
  - cicd
  - cicd/dokploy
---

# Dokploy – installation og setup

> **Dybere end dagens teori:** Trin for at få Dokploy op på serveren. Dag-note: [[../Noter/DoD - Pensum/Dag-08-Dokploy-og-GitHub]]. Overblik: [[Dokploy-overblik]]. Efter install: [[Dokploy-GitHub-og-webhooks]].

---

## Forudsætninger

- Server med **Docker** installeret (som I har fra [[../Noter/DoD - Pensum/Dag-03-Database-Setup-med-Docker]] og [[../Noter/DoD - Pensum/Dag-06-Docker-grundlæggende]]).
- Adgang via **SSH** og evt. Twingate.
- **Domæne eller subdomæne** (fx `dokploy.jeresdomæne.dk`) anbefales – så I kan åbne Dokploy sikkert med HTTPS (Nginx + Let's Encrypt som på Dag 4).

---

## Installationsskridt (kort)

1. **Installation** – Dokploy leveres typisk som **Docker-baseret** install: klon Dokploy’s repo eller brug deres install-script, der starter Dokploy som container(e) på serveren. Følg [Dokploy dokumentation](https://dokploy.com) eller underviserens anvisninger – kommandoer kan ændre sig mellem versioner.
2. **Første adgang** – Åbn Dokploy’s web interface (fx `https://dokploy.jeresdomæne.dk`). Opret admin-bruger. Sikr at port/firewall tillader adgang (evt. bag Nginx med Let's Encrypt).
3. **Konfiguration** – I Dokploy: konfigurér **server/agent** (hvor apps deployes – ofte samme maskine), og **build-metode** (Dockerfile, docker-compose) efter jeres projekt.

Når Dokploy kører og I kan logge ind, er næste skridt at **forbinde et GitHub-repository** – se [[Dokploy-GitHub-og-webhooks]].
