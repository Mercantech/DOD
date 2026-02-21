---
tags:
  - dod
  - docker
  - docker/database
---

# Database med Docker

> **Dybere end dagens teori:** Mere om database i container end vi når på Dag 3 – brug dette notat hvis I vil læse og øve mere. Dag-note: [[../Noter/DoD - Pensum/Dag-03-Database-Setup-med-Docker]]. Volumes: [[Volumes-og-data]]. Compose: [[Docker-Compose]].

---

## Hvorfor database i container?

- **Ensartethed:** Samme image og version på alle miljøer (lokalt, server).
- **Isolation:** Ingen direkte installation af PostgreSQL/MySQL på hosten.
- **Nem oprydning:** Stop og fjern container; data kan beholdes i et volume.

Se [[../Noter/DoD - Pensum/Dag-03-Database-Setup-med-Docker#Fordele ved database i container (vs. direkte på serveren)]].

---

## PostgreSQL i container

### Kun `docker run`

```bash
docker run -d \
  --name postgres \
  -e POSTGRES_USER=minbruger \
  -e POSTGRES_PASSWORD=hemmeligt \
  -e POSTGRES_DB=minapp \
  -p 5432:5432 \
  -v pgdata:/var/lib/postgresql/data \
  postgres:16-alpine
```

- **Miljøvariabler:** `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` – Postgres bruger dem ved første opstart og opretter bruger og database.
- **Port:** `5432:5432` – app på hosten eller anden container kan forbinde til `localhost:5432` (eller server-IP:5432).
- **Volume:** `pgdata` er et **named volume** – data overlever genstart. Uden volume er alt data væk, når containeren fjernes. Se [[Volumes-og-data]].

**Tjek at det kører:**
```bash
docker ps
docker exec -it postgres psql -U minbruger -d minapp -c "\dt"
```

---

## MySQL i container

```bash
docker run -d \
  --name mysql \
  -e MYSQL_ROOT_PASSWORD=roothemmeligt \
  -e MYSQL_DATABASE=minapp \
  -e MYSQL_USER=minbruger \
  -e MYSQL_PASSWORD=brugerhemmeligt \
  -p 3306:3306 \
  -v mysqldata:/var/lib/mysql \
  mysql:8
```

- **Port 3306** – standard for MySQL. Connection string fra app: `host=localhost` (eller `host=mysql` i Compose), port 3306, database `minapp`, bruger/password som sat.

---

## Forbindelse fra app (connection string)

- **App på hosten:** `host=localhost` (eller serverens IP), `port=5432` (Postgres) eller `3306` (MySQL), `user=...`, `password=...`, `database=...`.
- **App i anden container (samme Compose):** Brug **service-navnet** som host – fx `host=postgres` eller `host=db`. Compose opretter et netværk hvor servicenavne opløses til container-IP. Se [[Netværk-i-Docker]].

Eksempel (Postgres, fra app i Compose):
```
host=db port=5432 user=minbruger password=hemmeligt dbname=minapp
```

---

## Compose-eksempel til Dag 3

I **docker-mappen** ligger en `docker-compose.yml` I kan bruge på Dag 3: én **Postgres**-service med volume, og (valgfrit) en **app**-service der bygges fra en Dockerfile. Struktur:

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: proxi
      POSTGRES_PASSWORD: proxi
      POSTGRES_DB: proxi
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  pgdata:
```

**Kør:**
```bash
cd docker
docker compose up -d
```

Databasen er tilgængelig på `localhost:5432` med bruger `proxi`, password `proxi`, database `proxi`. Data persisteres i volume `pgdata` ([[Volumes-og-data]]). Når I tilføjer en app-service, kan den forbinde til `host=db`.

---

## Sikkerhed (kort)

- Brug **stærke passwords** – ikke `proxi`/`hemmeligt` i produktion.
- Eksponér **ikke** database-porten ud mod internettet, medmindre I har firewall og begrundelse. Typisk skal kun jeres app (på samme server eller i samme netværk) kunne ramme databasen.
