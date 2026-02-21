---
tags:
  - dod
  - docker
  - docker/network
---

# Netværk i Docker

> **Dybere end dagens teori:** Mere om netværk mellem containere end vi når på Dag 3 og Dag 7 – brug dette notat hvis I vil forstå hvordan app og database finder hinanden. Dag-noter: [[../Noter/DoD - Pensum/Dag-03-Database-Setup-med-Docker]], [[../Noter/DoD - Pensum/Dag-07-Docker-Compose]]. Compose: [[Docker-Compose]], [[Database-med-Docker]].

---

## Hvordan containere finder hinanden?

Når flere containere skal tale sammen (fx app → database), skal de være på **samme netværk**. I **Docker Compose** oprettes ét default-netværk per projekt, og hver **service** kan nå de andre via **service-navnet** som hostname.

- Eksempel: Service `db` (Postgres) og service `app` (jeres backend). I appens connection string sætter I `host=db` – Docker opløser `db` til containerens IP på Compose-netværket.
- Port mapping (`-p 5432:5432` eller `ports:` i Compose) bruges når *hosten* (eller verden udefra) skal nå containeren. Mellem containere på samme netværk behøver I ikke eksponere porten til hosten – I bruger bare service-navn og intern port (fx `db:5432`).

---

## Bridge-netværk (default)

Uden at definere `networks:` i Compose får alle services et **bridge-netværk** med et automatisk navn (fx `docker_default`). De kan alle nå hinanden via service-navn. På Linux-serveren er det typisk det I bruger til app + database.

---

## Host-netværk (avanceret)

`network_mode: host` gør at containeren deler hostens netværk direkte – ingen port mapping. Bruges nogle gange til performance eller specielle setup; normalt bruger I bridge og service-navne.

---

## Praktisk: Connection string fra app til database

- **App og db i samme Compose:** `host=db`, `port=5432` (Postgres) eller `3306` (MySQL). Se [[Database-med-Docker#Forbindelse fra app (connection string)]].
- **Kun db i Compose, app på hosten:** App forbinder til `host=localhost`, `port=5432`, fordi I har `ports: - "5432:5432"` på db-service.
