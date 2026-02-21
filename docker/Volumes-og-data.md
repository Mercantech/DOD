---
tags:
  - dod
  - docker
  - docker/volumes
---

# Volumes og data persistence i Docker

> **Dybere end dagens teori:** Mere om volumes end vi når på Dag 3 og Dag 9 – brug dette notat hvis I vil gå i dybden. Dag-noter: [[../Noter/DoD - Pensum/Dag-03-Database-Setup-med-Docker]], [[../Noter/DoD - Pensum/Dag-09-Volumes-Dokploy-og-Kubernetes]]. Compose: [[Docker-Compose]].

---

## Hvorfor volumes?

Containere er **efemære**: når du stopper og fjerner en container, er alt der kun lå inde i containeren væk. En database skriver data til fx `/var/lib/postgresql/data` – uden et **volume** vil al data være væk ved container-genstart eller -sletning. Med et volume ligger data på hosten og overlever.

---

## Named volume vs. bind mount

| Type | Beskrivelse | Typisk brug |
|------|-------------|-------------|
| **Named volume** | Docker administrerer en mappe. Du refererer til den med et navn. | Databaser, persisteret app-data. Nem i Compose. |
| **Bind mount** | Du mapper en konkret mappe på hosten ind i containeren. | Udvikling (live-sync af kode), præcis placering af data. |

**Eksempel named volume (Compose):**
```yaml
services:
  db:
    image: postgres:16-alpine
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

**Eksempel bind mount:**
```yaml
volumes:
  - ./data:/var/lib/postgresql/data
  - ./src:/app/src
```

---

## Kommandoer

- `docker volume ls` – vis alle volumes.
- `docker volume inspect <navn>` – vis hvor volumet ligger.
- `docker volume rm <navn>` – slet volume (containere må ikke bruge det).
- Ved `docker compose down`: named volumes bevares. Brug `docker compose down -v` for også at fjerne volumes.

---

## Dag 3 og Dag 9

- **Dag 3:** Database op med named volume (fx `pgdata`). Se [[Database-med-Docker]] og `docker-compose.yml` i denne mappe.
- **Dag 9:** Forskellen named vs. bind; i Kubernetes bruges PersistentVolumeClaim – samme idé. Se Dag 9-noten i Noter-mappen.
