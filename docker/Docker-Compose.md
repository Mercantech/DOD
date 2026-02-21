---
tags:
  - dod
  - docker
  - docker/compose
---

# Docker Compose

> **Dybere end dagens teori:** Dette notat går længere end vi når på Dag 3 og Dag 7 – brug det hvis I vil dykke ned i Compose. Dag-noter: [[../Noter/DoD - Pensum/Dag-03-Database-Setup-med-Docker]], [[../Noter/DoD - Pensum/Dag-07-Docker-Compose]]. Eksempel med database: [[Database-med-Docker]]. Volumes: [[Volumes-og-data]].

---

## Hvad er Docker Compose?

**Docker Compose** bruger en fil (typisk `docker-compose.yml`) til at beskrive **services** (containere), **volumes** og **netværk** i ét projekt. I stedet for at køre mange `docker run`-kommandoer, kører I `docker compose up` – Compose opretter netværk, volumes og starte alle services.

- **Kommandoer:** `docker compose up -d` (start i baggrunden), `docker compose down` (stop og fjern containere; `-v` fjerner også anonyme volumes), `docker compose ps`, `docker compose logs -f`.
- **Fil:** `docker-compose.yml` i projektroden. YAML-format med `services:`, `volumes:` og evt. `networks:`.

---

## Struktur af en Compose-fil

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: bruger
      POSTGRES_PASSWORD: hemmeligt
      POSTGRES_DB: minapp
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    restart: unless-stopped

  app:
    build: .
    ports:
      - "3000:3000"
    env_file: .env
    depends_on:
      - db
    restart: unless-stopped

volumes:
  pgdata:
```

- **services:** Hver nøgle (`db`, `app`) er en service. Compose opretter ét netværk per projekt, så `app` kan nå `db` via hostname `db`.
- **image** vs. **build:** `image` bruger et færdigt image; `build: .` bygger fra Dockerfile i nuværende mappe.
- **depends_on:** Compose starter `db` før `app`. Det sikrer ikke at databasen er *klar* til forbindelser, men at containeren er startet.
- **volumes:** Named volume `pgdata` – defineret under `volumes:` nederst. Se [[Volumes-og-data]].

---

## Miljøvariabler i Compose

- **environment:** Direkte key-value (som i eksemplet) eller liste: `POSTGRES_USER: bruger`.
- **env_file:** Filer som `.env` (én variabel per linje, `KEY=value`). Godt til at holde hemmeligheder uden for YAML.
- **Variabel-substitution:** I YAML kan du bruge `${VARIABEL}` – Compose udfylder fra shell eller `.env`.

---

## Netværk (standard)

Uden at definere `networks:` får alle services i samme Compose-fil automatisk adgang til et **default-netværk**. De kan nå hinanden via **service-navnet** som hostname (fx `db`, `app`). Derfor kan jeres app forbinde til databasen med `host=db` (i stedet for `localhost`), når både app og db kører i samme Compose-projekt.

---

## Praktisk workflow

1. Opret `docker-compose.yml` (evt. kopiér fra [[Database-med-Docker#Compose-eksempel til Dag 3]] eller `docker-compose.yml` i denne mappe).
2. `docker compose up -d --build` – byg (hvis der er `build:`), start alle services i baggrunden.
3. Tjek: `docker compose ps`, `docker compose logs -f app`.
4. Stop: `docker compose down`. Data i named volumes forbliver (brug `docker compose down -v` kun hvis I vil slette volumes).

Se også den færdige **[[00-Docker-overblik|docker-compose.yml]]** i docker-mappen som eksempel til Dag 3.
