---
tags:
  - dod
  - docker
---

# Docker – pensum og overblik

Dette er **Docker-pensum** til DoD-kurset. Mappen bruges sammen med [[../Noter/DoD - Pensum/Program]] og dag-noterne. Her finder I dybdegående teori, kommandoer og eksempler – især til [[Docker-grundlæggende]], [[Docker-Compose]], database og volumes. Alle noter i denne mappe kan linkes i Obsidian (samme vault som Noter).

> **Vil I dybere end hvad I når på en enkelt dag?** Hele denne mappe er **ekstra pensum** I kan dykke ned i. Hver note under matcher én eller flere dage – brug dem når I vil læse mere end dagens teori.

---

## Indhold i denne mappe

| Note | Indhold | Relevant for |
|------|---------|--------------|
| **[[Docker-grundlæggende]]** | Images, containere, grundkommandoer, Docker Desktop vs. Linux | Dag 3, Dag 6 |
| **[[Docker-Compose]]** | Compose-filer, services, netværk, `up`/`down` | Dag 3, Dag 6, Dag 7 |
| **[[Database-med-Docker]]** | PostgreSQL og MySQL i container med konkrete eksempler | **Dag 3** |
| **[[Volumes-og-data]]** | Named volumes, bind mounts, persistence | Dag 3, **Dag 9** |
| **[[Dockerfile-praksis]]** | Bygge egne images, multi-stage, .dockerignore | Dag 6, Dag 7 |
| **[[Netværk-i-Docker]]** | Netværk mellem containere, bridge, service-navne | Dag 3, Dag 7 |

---

## Eksempler i mappen

- **`docker-compose.yml`** – Færdigt eksempel med Postgres (og valgfri app), til brug på [[../Noter/DoD - Pensum/Dag-03-Database-Setup-med-Docker|Dag 3]] og til at øve Compose. Se [[Database-med-Docker]] (sektion "Compose-eksempel til Dag 3").

---

## Sådan hænger det sammen med kurset

- **Uge 24, Dag 3:** Database i container – brug [[Database-med-Docker]] og [[Docker-grundlæggende]]. Eksempel: `docker-compose.yml` i denne mappe. Dag-note: [[../Noter/DoD - Pensum/Dag-03-Database-Setup-med-Docker]].
- **Uge 25, Dag 6–7:** Dockerfile og Compose – brug [[Dockerfile-praksis]] og [[Docker-Compose]]. Dag-noter: [[../Noter/DoD - Pensum/Dag-06-Docker-grundlæggende]], [[../Noter/DoD - Pensum/Dag-07-Docker-Compose]].
- **Uge 25, Dag 9:** Volumes og persistence – brug [[Volumes-og-data]] og [[../Noter/DoD - Pensum/Dag-09-Volumes-Dokploy-og-Kubernetes]].

**Kort:** Start i dag-noterne (Noter-mappen); når I vil have **mere dybde**, er Docker-mappen her til netop det.
