# Dag 6 – Docker grundlæggende

> Teori til Dag 6 (15. juni). I dag sætter I *jeres* egen app i en container – fra Dockerfile til kørende container. Se [[Program]] for dagens mål og plan. **Mere pensum:** [[../../docker/00-Docker-overblik]], [[../../docker/Docker-grundlæggende]], [[../../docker/Dockerfile-praksis]].

---

## Docker installation og verifikation

På Dag 6 arbejder I med Docker på **serveren** (Linux) – det er her jeres app-container skal køre i drift. I kan også øve lokalt med Docker Desktop; kommandoerne er de samme.

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install docker.io
sudo systemctl enable docker
sudo systemctl start docker
```

**Verificer at Docker kører:**
```bash
docker --version
docker run hello-world
```

- `hello-world` er et minimalt image: Docker henter det (hvis nødvendigt), starter en container der printer en besked og afslutter. Hvis det virker, er Docker-installationen i orden.
- På serveren kan det være nødvendigt at tilføje jeres bruger til gruppen `docker` (`sudo usermod -aG docker $USER`) så I kan køre `docker` uden `sudo` – log ud og ind igen efterpå.

Se også [[../../docker/Docker-grundlæggende#Installation]] og sammenligning Docker Desktop vs. Linux i docker-pensum.

---

## Image og container – forskel og sammenhæng

- **Image** = en **frossen skabelon**. Det indeholder filsystem (OS-lag, app-filer, afhængigheder) og metadata (fx hvilken kommando der skal køre ved start). Images er **read-only** og deles mellem alle containere der kører fra dem. Eksempler: `postgres:16-alpine`, `node:20-alpine`, eller et image I selv bygger fra en Dockerfile.
- **Container** = en **kørende instans** af et image. Hver gang I kører `docker run <image>`, oprettes en ny container. Containeren har et skrivbart lag oven på image – ændringer (fx filer skrevet under kørsel) ligger kun i containeren og **forsvinder** når containeren fjernes, medmindre I bruger **volumes** (Dag 9).

**Sammenhængen:** Ét image kan bruges til mange containere. Ændringer i en container ændrer **ikke** image. For at opdatere "appen" bygger I et nyt image (fra Dockerfile) og starter en ny container fra det. Derfor er Dockerfile og `docker build` centrale på Dag 6.

---

## Dockerfile – skrivning og bygge

En **Dockerfile** beskriver trin for trin hvordan et image skal bygges: hvilket base image, hvilke filer der kopieres ind, hvilke kommandoer der kører ved **build**, og hvilken kommando der kører når containeren **starter** (CMD/ENTRYPOINT).

### Grundlæggende instruktioner

| Instruktion | Betydning |
|-------------|-----------|
| **FROM** | Base image (fx `node:20-alpine`, `python:3.12-slim`). Alt bygges oven på dette. |
| **WORKDIR** | Sætter arbejdsmappen inde i containeren. Efterfølgende RUN, COPY, CMD udføres her. |
| **COPY** | Kopiérer filer fra **build-konteksten** (den mappe I kører `docker build` fra) ind i image. |
| **RUN** | Kører en kommando **ved build** (fx `npm install`, `pip install`). Ændringer bliver en del af image. |
| **EXPOSE** | Dokumenterer hvilken port appen lytter på. Åbner **ikke** porten – det gør `-p` ved `docker run` eller `ports:` i Compose. |
| **CMD** | Standard kommando når containeren **startes**. Kun én CMD; ofte formen `["executable", "arg1", "arg2"]`. |

**Build-kontekst:** Når I kører `docker build -t mitimage:tag .`, er **punktumet** konteksten – altså den mappe hvor Dockerfile ligger og hvorfra COPY henter filer. Store mapper (fx `node_modules`) bør udelukkes med **.dockerignore** for hurtigere build og mindre image.

### Eksempel: Node-app

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3000
CMD ["node", "server.js"]
```

- Først kopieres kun `package.json` (og package-lock) og kører `npm ci` – så lagres afhængigheder i et eget lag og caches bedre ved næste build hvis kun koden ændres.
- Derefter kopieres resten af koden. `EXPOSE 3000` fortæller at appen lytter på 3000; ved `docker run` bruger I fx `-p 3000:3000` for at åbne porten.

### Eksempel: Python/FastAPI-app

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

- Base image med Python; `requirements.txt` kopieres og pakker installeres før resten af koden.
- `uvicorn` kører FastAPI-appen. `--host 0.0.0.0` sikrer at serveren lytter på alle interfaces (så den kan nås udefra containeren).

Flere detaljer og multi-stage builds: [[../../docker/Dockerfile-praksis]].

---

## Build og run – workflow

**Bygge image:**
```bash
docker build -t minapp:latest .
```

- `-t minapp:latest` giver image et **tag** (navn og evt. version). Uden tag får image et langt ID.
- `.` er build-konteksten (nuværende mappe). Dockerfile skal ligge her (eller angives med `-f`).

**Køre container:**
```bash
docker run -d -p 3000:3000 --name minapp-container minapp:latest
```

- `-d`: kør i baggrunden (detached).
- `-p 3000:3000`: map hostens port 3000 til containeren 3000 – så I kan åbne `http://localhost:3000` (eller server-IP:3000).
- `--name`: giv containeren et navn så I nemt kan `docker stop minapp-container`, `docker logs minapp-container` osv.

**Tjek og fejlsøgning:**
- `docker ps` – vis kørende containere.
- `docker logs minapp-container` – vis output fra appen.
- `docker exec -it minapp-container sh` – åbn shell inde i containeren (fx for at tjekke filer eller miljø).

Når I ændrer koden, bygger I igen (`docker build -t minapp:latest .`) og stopper/fjerner den gamle container og starter en ny fra det nye image. Senere på kurset automatiserer I det med Compose og Dokploy. Et komplet eksempel hvor Docker bruges til at *bygge* images som derefter kører i Kubernetes (K3s) findes i **[[Proxi-demo]]**.

---

## Læringsmål (opsummering)

1. Installere Docker på en server og verificere at det fungerer korrekt (fx med `docker run hello-world`).
2. Skrive og bygge en Dockerfile til en simpel applikation (FROM, WORKDIR, COPY, RUN, EXPOSE, CMD – og evt. .dockerignore).
3. Forklare forskellen på image og container, og hvordan de hænger sammen (image = skabelon, container = kørende instans; én image, mange containere; ændringer i container ændrer ikke image).
