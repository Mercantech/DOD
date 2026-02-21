# Dag 7 – Docker Compose & Multi-container

> Teori til Dag 7 (16. juni). I dag får I *jeres* full-stack app og database til at køre sammen med én fil og én kommando. Se [[Program]] for dagens mål og plan. **Mere pensum:** [[../../docker/Docker-Compose]], [[../../docker/Database-med-Docker]], [[../../docker/Volumes-og-data]], [[../../docker/Netværk-i-Docker]].

---

## Hvad er Docker Compose?

**Docker Compose** bruger en enkelt fil – typisk `docker-compose.yml` – til at beskrive **flere containere** (services), deres **volumes** og **netværk** i ét projekt. I stedet for at køre mange `docker run`-kommandoer manuelt, kører I **én kommando**: `docker compose up`. Compose opretter netværket, starter databasen, bygger og starter appen, og kobler dem sammen.

- **Praktisk:** I kan have både **database** og **app** defineret i samme fil. Appen kan forbinde til databasen via **service-navnet** (fx `db`) som hostname – Compose sørger for at de er på samme netværk.
- **Kommandoer:** `docker compose up -d` (start i baggrunden), `docker compose up -d --build` (genbyg images og start), `docker compose down` (stop og fjern containere), `docker compose ps`, `docker compose logs -f app`.

---

## Skrive en docker-compose.yml med app og database

Strukturen er: **services** (hver container), og evt. **volumes** og **networks**. Her er et typisk setup med Postgres og jeres app.

### Eksempel – database + app

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
    environment:
      NODE_DB_HOST: db
      NODE_DB_PORT: "5432"
      NODE_DB_USER: bruger
      NODE_DB_PASSWORD: hemmeligt
      NODE_DB_NAME: minapp
    depends_on:
      - db
    restart: unless-stopped

volumes:
  pgdata:
```

- **db:** Bruger færdigt image `postgres:16-alpine`. `environment` sætter bruger, password og databasenavn. **volumes** sikrer at data overlever genstart ([[../../docker/Volumes-og-data]]). Port 5432 eksponeres så I evt. kan forbinde fra hosten (fx med et værktøj).
- **app:** `build: .` betyder at image bygges fra Dockerfile i nuværende mappe (som på Dag 6). **environment** giver appen forbindelsesdata til databasen – her med **host = db**, fordi `db` er service-navnet og Compose opløser det til database-containeren på det fælles netværk.
- **depends_on: db:** Compose starter `db` før `app`. Det betyder ikke at Postgres er *klar* til forbindelser (der kan gå et par sekunder), men at containeren er startet – mange apps håndterer "retry" ved opstart.
- **volumes: pgdata:** Named volume så database-data ikke forsvinder ved `docker compose down`.

### Hvad I skal tilpasse

- **db:** Byt `POSTGRES_*` og evt. port hvis I bruger MySQL eller andet.
- **app:** Sørg for at jeres app læser **environment variables** til database-forbindelse (fx `NODE_DB_HOST`, `DATABASE_URL` eller det jeres framework forventer). Sæt `NODE_DB_HOST=db` (eller `DATABASE_HOST=db`) – **ikke** `localhost`, fordi appen kører i sin egen container og `localhost` der peger på app-containeren selv.

---

## Environment variables på tværs af containere

Compose giver to hovedmåder at styre opsætning på:

### 1. Direkte i YAML: `environment:`

```yaml
app:
  environment:
    NODE_DB_HOST: db
    NODE_DB_PORT: "5432"
    NODE_ENV: production
```

- Simpelt og tydeligt. **Ulempe:** Hemmeligheder (passwords) står i filen – så lad dem **ikke** committe med kode. Brug i stedet `env_file` eller fil-mount til secrets.

### 2. Via fil: `env_file:`

```yaml
app:
  env_file: .env
  # eller
  env_file:
    - .env
    - .env.production
```

- I `.env` (som **ikke** må ligge i Git):  
  `NODE_DB_HOST=db`  
  `NODE_DB_PASSWORD=hemmeligt`
- Compose læser filen og sætter variablerne i app-containeren. Så kan I have forskellige `.env` lokalt og på serveren uden at ændre YAML.

### 3. Variabel-substitution i YAML

I selve `docker-compose.yml` kan I bruge `${VARIABEL}` – fx `${DB_PASSWORD}`. Compose udfylder fra shell-miljøet eller fra en `.env`-fil i samme mappe. Godt til at undgå at skrive hemmeligheder direkte i YAML.

**Vigtigt:** Appen får **kun** de variabler der er sat i *dens* service (environment eller env_file). Database-containeren kender ikke appens variabler – og omvendt. Det er jer der sætter fx `NODE_DB_HOST=db` så appen ved hvor databasen er (service-navnet `db`).

---

## Hvorfor Compose gør det nemmere at arbejde med flere services

| Uden Compose | Med Compose |
|--------------|-------------|
| Flere `docker run`-kommandoer med præcis port, volume og netværk | Én fil beskriver alt; `docker compose up` |
| Manuel oprettelse af netværk og tjek af container-navne | Compose opretter netværk og giver service-navne som hostname (`db`, `app`) |
| Sværere at huske rækkefølge (database før app) | `depends_on` styrer startrækkefølge |
| Volumes og ports skal matches manuelt | Volumes og ports er defineret ét sted i YAML |

Kort sagt: **én fil, én kommando**, og alle services kan tale sammen via service-navne. Det gælder både lokalt og på serveren – samme `docker-compose.yml` kan bruges til udvikling og til enkel deployment (senere suppleres det evt. med Dokploy eller anden CI/CD). Et demo-projekt der bruger Compose til app+db og også viser samme idé i Kubernetes: **[[Proxi-demo]]**.

---

## Praktisk workflow

1. Opret `docker-compose.yml` i projektroden (samme mappe som Dockerfile for appen). Brug eksemplet ovenfor eller [[../../docker/Database-med-Docker#Compose-eksempel til Dag 3]] / `docker/docker-compose.yml`.
2. Sørg for at jeres app læser database-config fra environment (fx `NODE_DB_HOST`, `DATABASE_URL`). Sæt host til **db** (service-navnet).
3. Kør: `docker compose up -d --build` – Compose bygger app-image, starter db og app, og forbinder dem.
4. Tjek: `docker compose ps` (begge kører?), `docker compose logs -f app` (fejl?).
5. Stop: `docker compose down`. Named volumes bevares – data i databasen er der stadig næste gang I kører `up`.

---

## Læringsmål (opsummering)

1. Skrive en `docker-compose.yml` der starter både en app og en database (services, image/build, ports, volumes, depends_on).
2. Bruge environment variables til at styre opsætning på tværs af containere – fx `environment:` eller `env_file:`, og sætte appens database-host til service-navnet (`db`).
3. Forklare hvordan Docker Compose gør det nemmere at arbejde med flere services: én fil, én kommando, fælles netværk med service-navne, depends_on og genbrugelig konfiguration.
