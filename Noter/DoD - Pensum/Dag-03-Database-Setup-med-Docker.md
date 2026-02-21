# Dag 3 – Database Setup med Docker

> Teori til Dag 3 (10. juni). Her får *jeres* app en database der kører stabilt i en container – klar til at jeres backend eller full-stack app kan forbinde. Se [[Program]] for dagens mål og plan. **Mere Docker-pensum og eksempler:** [[../../docker/00-Docker-overblik]] og [[../../docker/Database-med-Docker]] (Compose-eksempel i `docker/docker-compose.yml`).

---

## Docker Desktop og Docker på Linux (server)

På Dag 3 kigger I på Docker på **to måder**: **Docker Desktop** (på jeres egen pc) og **Docker på en Linux-server**. Begge kan køre de samme images og containere – men brugen er forskellig.

| | Docker Desktop | Docker på Linux (server) |
|--|----------------|---------------------------|
| **Hvor** | Windows/macOS (lokalt på jeres maskine) | Ubuntu/Debian-server (fx den I fik adgang til på Dag 1) |
| **Interface** | Grafisk UI (containere, images, logs, terminal) + `docker` i kommandolinjen | Kun kommandolinje: `docker`, `docker compose` |
| **Typisk brug** | Udvikling, hurtig test af containere og databaser lokalt, bygge images | Det sted hvor *jeres* app og database rent faktisk kører for andre (produktion/drift) |
| **Installation** | Download fra docker.com, installér, start Docker Desktop | `apt install docker.io` (eller officiel Docker-pakke), `systemctl enable docker` |

**Hvorfor begge dele:** Lokalt med Docker Desktop kan I prøve database-containere og kommandoer uden at røre serveren. På Linux-serveren sætter I den Docker, der *tæller* for jeres deployment – her kører databasen og senere jeres app. Samme kommandoer (`docker run`, `docker ps` osv.) gælder begge steder, så det I lærer lokalt kan I bruge på serveren.

---

## Docker – kort gennemgang

**Docker** kører applikationer i **containere**: isolerede miljøer med eget filsystem og netværk, men delt operativsystemskerne. Du beskriver hvad der skal køre i en **image** (fx bygget fra en Dockerfile eller hentet fra Docker Hub); Docker starter en **container** ud fra det image.

- **Installation på Linux (server):** På Ubuntu/Debian typisk `sudo apt update`, `sudo apt install docker.io` (eller den officielle Docker-pakke). Efter install: `sudo systemctl enable docker`, `sudo systemctl start docker`. Tjek med `docker run hello-world`.
- **Docker Desktop:** Installér fra [docker.com](https://www.docker.com/products/docker-desktop/); efter start kan I bruge både UI’en og `docker` i terminalen som på Linux.
- **Grundkommandoer (begge steder):** `docker pull <image>` (hent image), `docker run [options] <image>` (start container), `docker ps` (vis kørende containere), `docker stop <container>`, `docker rm <container>`.

På Dag 3 bruger I Docker til at køre en **database-container** – lokalt i Desktop til at øve, og på Linux-serveren som det miljø der tæller for jeres app.

---

## Database i container (PostgreSQL / MySQL)

Både **PostgreSQL** og **MySQL** (og fx MariaDB) findes som officielle images på Docker Hub. I kører én container med databasen og konfigurerer den med **miljøvariabler** (bruger, password, databasenavn). Data bør ligge i et **volume** (som I dykker dybere ned i på Dag 9), så databasen overlever genstart af containeren.

### Eksempel: PostgreSQL

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

- `-d`: kør i baggrunden (detached).
- `-e`: miljøvariabler – her bruger, password og db-navn som Postgres bruger ved opstart.
- `-p 5432:5432`: port mapping – hostens 5432 mappes til containeren 5432, så andre (fx jeres app) kan forbinde til `localhost:5432` eller server-IP:5432.
- `-v pgdata:/var/lib/postgresql/data`: volume så data persisteres (vigtigt i produktion).
- `postgres:16-alpine`: image og tag fra Docker Hub.

### Eksempel: MySQL

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

- Port **3306** er MySQLs standard. `MYSQL_DATABASE` opretter databasen ved første start; `MYSQL_USER` og `MYSQL_PASSWORD` giver en bruger med adgang til den.

---

## Konfiguration og forbindelse fra eksterne services

- **Inde i containeren:** Databasen lytter på sin normale port (5432 for Postgres, 3306 for MySQL). Bruger, password og databasenavn er det I sat med `-e`.
- **Fra hosten eller andre containere:** Hvis I eksponerer porten med `-p 5432:5432`, kan en app der kører på **samme server** forbinde til `localhost:5432` (eller serverens IP) med de samme bruger/password/db-navn.
- **Fra en anden container (samme host):** I kan sætte begge containere på samme **Docker-netværk** (`docker network create minnet`, `docker run --network minnet ...`). Så kan app-containeren forbinde til **service-navnet** (fx `postgres`) som hostname – Docker opløser det til containerens IP. Connection string bliver fx `host=postgres port=5432 user=minbruger password=hemmeligt dbname=minapp`.
- **Sikkerhed:** Brug stærke passwords og eksponér ikke database-porten ud mod internettet, medmindre I har god grund (fx firewall der kun tillader bestemte IP’er). Typisk skal kun jeres app på serveren (eller i samme netværk) kunne ramme databasen.

---

## Fordele ved database i container (vs. direkte på serveren)

| Aspekt | Container | Direkte på server |
|--------|-----------|--------------------|
| **Installation** | Én `docker run` (eller Compose); samme image overalt. Ingen manuel pakke-/versionstyring på host. | Pakker skal installeres og opdateres per server; forskellige versioner kan give uoverensstemmelser. |
| **Isolation** | Database og dens filer er i containeren (evt. volume); konflikter med andre tjenester er mindre. | Deler server med alt andet; konfiguration kan påvirke hele systemet. |
| **Flytbarhed** | Samme image og env kører på andre servere eller i Kubernetes; nemmere at replicere miljøet. | Kræver dokumentation og manuel opsætning hver gang. |
| **Oprydning** | Stop og fjern container (data i volume kan beholdes); serveren er "ren" uden database-pakker. | Afinstallering og rydding er mere indgribende. |

Kort sagt: containere giver **ensartethed**, **isolation** og **nemmere genbrug** af jeres database-miljø – især når I senere bruger Docker Compose eller Kubernetes og vil have samme setup på flere maskiner.

---

## Læringsmål (opsummering)

1. Installere Docker og køre en container med en database (PostgreSQL, MySQL eller alternativ).
2. Konfigurere adgang og forbindelser til databasen fra eksterne services (port, netværk, connection string).
3. Forklare fordelene ved at køre databaser i containere frem for direkte på serveren.
