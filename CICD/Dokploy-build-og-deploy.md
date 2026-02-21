---
tags:
  - dod
  - cicd
  - cicd/dokploy
---

# Dokploy – build og deploy

> **Dybere end dagens teori:** Hvordan Dokploy bygger og deployer, env vars og typiske fejl. Dag-noter: [[../Noter/DoD - Pensum/Dag-08-Dokploy-og-GitHub]], [[../Noter/DoD - Pensum/Dag-09-Volumes-Dokploy-og-Kubernetes]]. Docker-pensum: [[../docker/Dockerfile-praksis]], [[../docker/Docker-Compose]].

---

## Dockerfile vs. Docker Compose i Dokploy

- **Dockerfile:** Dokploy kører `docker build` (evt. med context og Dockerfile-sti I angiver) og starter én container fra det image. Typisk til enkelt-app eller når I selv håndterer database andetsteds.
- **Docker Compose:** Dokploy bruger jeres `docker-compose.yml` – bygger evt. med `build:`, starter alle services (app + database). Bedre til full-stack med database i samme projekt.

Vælg den type der matcher jeres repo (én app vs. app + db i Compose).

---

## Environment variables

- I Dokploy konfigurerer I **environment variables** til at køre på serveren – fx database-URL, API-nøgler. De skal **ikke** stå i koden; de sættes i Dokploy’s UI (eller i compose som secrets).
- **Build-argumenter** (ARG) kan bruges under build hvis I har brug for det; **runtime**-konfiguration er typisk **env vars** (ENV i container).

---

## Build-logs og typiske fejl

- **Build fejler:** Kig i Dokploy’s **build-logs** – ofte manglende afhængigheder, forkert Dockerfile-sti, eller fejl i Dockerfile (fx COPY fejler). Sammenlign med at køre `docker build` lokalt.
- **Container starter ikke / crasher:** Kig i **runtime-logs** (Logs for containeren). Ofte manglende env var, forkert database-URL, eller port allerede i brug.
- **Webhook udløser ikke:** Tjek i GitHub at webhook’en er tilføjet og at "Recent Deliveries" viser 200. Tjek at branch i Dokploy matcher den I pusher til.

Se [[Dokploy-volumes-og-monitoring]] for volumes og logs; [[Deployment-automatisering-praksis]] for rollback og best practices.
