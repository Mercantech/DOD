---
tags:
  - dod
  - docker
---

# Docker – grundlæggende

> **Dybere end dagens teori:** Dette notat dækker mere end vi når på Dag 3 og Dag 6 – brug det hvis I vil læse videre. Dag-noter: [[../Noter/DoD - Pensum/Dag-03-Database-Setup-med-Docker]], [[../Noter/DoD - Pensum/Dag-06-Docker-grundlæggende]]. Compose og volumes: [[Docker-Compose]], [[Volumes-og-data]].

---

## Hvad er Docker?

**Docker** kører applikationer i **containere**: isolerede miljøer med eget filsystem og netværk, men delt operativsystemskerne (Linux-kernen). Du beskriver hvad der skal køre i et **image**; Docker starter en **container** ud fra det image.

- **Image** = frossen skabelon (fx `postgres:16-alpine`, `nginx:alpine`). Hentes fra Docker Hub eller bygges fra en Dockerfile.
- **Container** = kørende instans af et image. Data *inden i* containeren er efemær, medmindre du bruger **volumes** (se [[Volumes-og-data]]).

---

## Docker Desktop vs. Docker på Linux (server)

| | Docker Desktop | Docker på Linux (server) |
|--|----------------|---------------------------|
| **Hvor** | Windows/macOS (lokalt) | Ubuntu/Debian-server |
| **Interface** | GUI + `docker` i terminal | Kun CLI: `docker`, `docker compose` |
| **Brug** | Udvikling, test, bygge images | Produktion – her kører jeres app og database |

Samme kommandoer gælder begge steder.

---

## Installation

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install docker.io
sudo systemctl enable docker
sudo systemctl start docker
docker run hello-world
```

**Docker Desktop:** Download fra docker.com, installér og start.

---

## Grundkommandoer

| Kommando | Beskrivelse |
|----------|-------------|
| `docker pull <image>` | Hent image fra Docker Hub |
| `docker run [options] <image>` | Start en ny container |
| `docker ps` | Vis kørende containere. `docker ps -a` inkluderer stoppede. |
| `docker stop <container>` | Stop container |
| `docker rm <container>` | Fjern container |
| `docker logs <container>` | Vis logs |
| `docker exec -it <container> <cmd>` | Kør kommando inde i containeren |

### Typiske docker run-options

- `-d` – kør i baggrunden (detached).
- `--name <navn>` – giv containeren et navn.
- `-e KEY=value` – miljøvariabel.
- `-p hostport:containerport` – port mapping.
- `-v volume_eller_mappe:sti_i_container` – volume (se [[Volumes-og-data]]).

**Eksempel (Postgres):**
```bash
docker run -d --name postgres \
  -e POSTGRES_USER=bruger -e POSTGRES_PASSWORD=hemmeligt -e POSTGRES_DB=minapp \
  -p 5432:5432 \
  -v pgdata:/var/lib/postgresql/data \
  postgres:16-alpine
```

---

## Image vs. container

- **Image** = read-only. Ændringer i en kørende container ændrer ikke image.
- **Container** = kører fra et image. Når du sletter containeren, er alt der kun var i containeren væk – derfor volumes til database-data ([[Volumes-og-data]], [[Database-med-Docker]]).
