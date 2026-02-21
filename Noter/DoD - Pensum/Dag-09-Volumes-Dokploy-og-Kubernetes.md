---
tags:
  - dod
  - cicd
  - cicd/dokploy
---

# Dag 9 – Docker Volumes, Data Persistence og Kubernetes (k3s)

> Teori til Dag 9 (18. juni). Volumes, persistence og Dokploy er med til at *jeres* app kører stabilt og deployes automatisk ved push – vi bruger **Proxi**-demoen som eksempel (K3s-manifester og Docker Compose). Se [[Program]] for dagens mål og plan. **Dybere pensum:** [[../../CICD/00-CICD-overblik]] (Dokploy volumes, build, monitoring).

---

## Docker Volumes og data persistence

En container er **efemær**: når du stopper og fjerner den, er alt, der kun lå i containeren, væk. For en database (eller anden data) skal data **leve uden for** selve containeren, så de overlever genstart og ny container.

Det løser du med **volumes** (eller bind mounts): du kobler et stykke lagring (et "volume" eller en mappe på hosten) ind i containeren på en bestemt sti.

---

### Named volumes vs. bind mounts

| Type | Beskrivelse | Eksempel |
|------|-------------|----------|
| **Named volume** | Docker administrerer en mappe (typisk under `/var/lib/docker/volumes/`). Du refererer til den med et navn. Data overlever container-genstart og er nem at bruge i Compose. | `volumes: - pgdata:/var/lib/postgresql/data` |
| **Bind mount** | Du mapper en **konkret mappe på hosten** ind i containeren. Godt til udvikling (live-sync af kode) eller når du vil styre præcis hvor data ligger. | `volumes: - ./data:/var/lib/postgresql/data` |

I praksis: brug **named volumes** til databaser og anden persisteret data i produktion-lignende setup. Brug **bind mounts** når du vil mounte kode eller en bestemt mappe.

---

### Eksempel fra Proxi – Docker Compose med volume

I Proxi-demoen ligger der en `docker-compose.yml` med Postgres og en **named volume** til database-data:

```yaml
services:
  db:
    image: postgres:16-alpine
    volumes:
      - pgdata:/var/lib/postgresql/data
    # ...

volumes:
  pgdata:
```

- **pgdata** er et named volume. Docker opretter det første gang du kører `docker compose up`.
- Postgres skriver al data til `/var/lib/postgresql/data` inde i containeren – og den mappe er netop **pgdata**-volumet.
- Når du genstarter eller fjerner db-containeren og starter den igen, er data stadig der, fordi de ligger i volumet, ikke kun i containeren.

**Kommandoer du kan bruge:**
- `docker volume ls` – viser alle volumes.
- `docker volume inspect pgdata` – viser hvor volumet fysisk ligger på hosten.

---

## Kubernetes (K3s) – idéen og hvordan Proxi bruger det

**Kubernetes** er en platform til at køre containere: du beskriver *hvad* du vil have (app, database, adgang), og K8s sørger for at starte pods, genstarte ved fejl og distribuere trafik.

**K3s** er en letvægtsvariant: én binær med API server, kubelet, containerd, Traefik (ingress) og netværk. Perfekt til små clusters og læring. I Proxi kører K3s på VM’er (1 control plane + 2 workers) oprettet med Terraform og konfigureret med Ansible.

---

### Vigtige K8s-ressourcer (som I ser i Proxi)

| Ressource | Beskrivelse | I Proxi |
|-----------|-------------|---------|
| **Namespace** | Virtuelt rum til at gruppere ressourcer. | `proxi` – alt app og db ligger her. |
| **PersistentVolumeClaim (PVC)** | "Jeg har brug for X GB disk." Cluster tildeler et volume; data overlever pod-genstart. | Postgres bruger `postgres-pvc` (2 Gi). |
| **Deployment** | Beskriver app: image, antal replicas, env, volumeMounts. Opretter og holder pods kørende. | `proxi-app` (3 replicas), `postgres` (1 replica). |
| **Pod** | Mindste køreenhed – én eller flere containere. | Hver app-replica er en pod. |
| **Service** | Fast netværksnavn (ClusterIP) til pods. Andre pods når fx databasen via `proxi-db:5432`. | `proxi-db`, `proxi-app`. |
| **Ingress** | Regler for indgående HTTP. Traefik (i K3s) sender trafikken til den rigtige Service. | `/` → `proxi-app:80`. |

---

### Data persistence i Kubernetes – PVC i Proxi

I Proxi’s K8s-manifester (`app/k8s/postgres.yaml`) ser I et **PersistentVolumeClaim** og hvordan Postgres bruger det:

**1. Krav om disk (PVC):**
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
  namespace: proxi
spec:
  accessModes: [ReadWriteOnce]
  resources:
    requests:
      storage: 2Gi
```

**2. Postgres-Deployment mount’er volumet:**
```yaml
volumeMounts:
  - name: data
    mountPath: /var/lib/postgresql/data
volumes:
  - name: data
    persistentVolumeClaim:
      claimName: postgres-pvc
```

- K3s tildeler 2 GB til `postgres-pvc`. Data i `/var/lib/postgresql/data` ligger på det volume.
- Når Postgres-poden genstartes (eller flyttes), følger PVC’en med – data overlever.

Det svarer til at bruge et **named volume** i Docker, men her styres det af Kubernetes og kan bruges på tværs af pod-genstart og noder (inden for ReadWriteOnce-begrænsningen).

---

### App + database + adgang – flow i Proxi

- **App-pods** (3 stk) henter forbindelsesdata fra et **Secret** (`proxi-db`) og forbinder til `NODE_DB_HOST=proxi-db` (Service-navnet).
- **Postgres** kører som én pod med PVC; Service `proxi-db` giver et stabilt navn (`proxi-db.proxi.svc.cluster.local`) på port 5432.
- **Ingress** (Traefik) sender HTTP-trafik til `proxi-app`-Service, som round-robin til de 3 app-pods.

I kan åbne appen på http://\<control-plane-ip\> og genindlæse for at se skifte mellem pods. Det viser, at load fordeles på flere replicas.

---

### Docker Swarm – kort

**Docker Swarm** er Docker’s indbyggede orchestrator: flere maskiner danner et "swarm", og du deployer services (containere) som kan skaleres og genstartes. Konceptet minder om Kubernetes (replicas, services, netværk), men er enklere og mindre funktionsrig. Mange bruger i dag Kubernetes (eller K3s) i stedet for Swarm. Idéen er den samme: du beskriver ønsket tilstand, og systemet sørger for at holde den.

---

## Dokploy, Git og automatisk deployment

På Dag 9 arbejder I også med **Dokploy**: web interface til at deploye apps fra Git, med webhook så et **push til GitHub** udløser automatisk genbuild og deploy.

- **Dokploy** forbinder til jeres GitHub-repository og kan bygge fra Dockerfile eller docker-compose.
- Når I slår **webhook** til, sender GitHub en anmodning til Dokploy ved hvert push – Dokploy bygger og deployer derefter.
- Det giver en simpel **CI/CD**-agtig pipeline: push → build → deploy, uden at I selv skal logge ind på serveren og køre kommandoer.

Proxi-demoen viser et andet flow (Ansible + K3s), men målet er det samme: **fra kode til kørende app** ved hjælp af værktøjer og automation.

---

## Læringsmål (opsummering)

1. Oprette volumes i Docker og forbinde dem til en container (fx som i Proxi’s `docker-compose.yml` med `pgdata`).
2. Sikre, at data i databasen overlever en genstart af containeren – med named volume (Docker) eller PVC (Kubernetes).
3. Forklare forskellen på bind mounts og named volumes i praksis.
4. Forstå idéen med Docker Swarm og Kubernetes (k3s) – orchestrering, Deployments, Services, Ingress og persistence med PVC – med Proxi som eksempel.

---

## Proxi – hvad I får og hvor det ligger

Se **[[Proxi-demo]]** for Proxi’s plads i kurset og links til al dokumentation.

- **Repo og dokumentation:** Proxi sendes til jer som demo. Brug **[[Koncepter-og-overblik]]**, **[[K3s-og-Postgres]]** og **[[Deploy-og-rollout]]** (i Proxi/docs) til overblik og koncepter.
- **Docker volumes:** `app/docker-compose.yml` – Postgres med `pgdata`-volume.
- **K3s-manifester:** `app/k8s/` – `namespace.yaml`, `db-secret.yaml`, `postgres.yaml` (PVC + Deployment + Service), `app.yaml` (Deployment + Service), `ingress.yaml`. Se `app/k8s/README.md` for rækkefølge og `kubectl apply`.
