---
tags:
  - dod
  - docker
  - docker/dockerfile
---

# Dockerfile og bygge egne images

> **Dybere end dagens teori:** Mere om Dockerfile og multi-stage builds end vi når på Dag 6 og Dag 7 – brug dette notat hvis I vil bygge mere avancerede images. Dag-noter: [[../Noter/DoD - Pensum/Dag-06-Docker-grundlæggende]], [[../Noter/DoD - Pensum/Dag-07-Docker-Compose]]. Compose med `build:`: [[Docker-Compose]].

---

## Hvad er en Dockerfile?

En **Dockerfile** er en tekstfil der beskriver hvordan et **image** skal bygges: hvilket base image, hvilke filer der kopieres ind, hvilke kommandoer der kører ved build, og hvad der kører når containeren starter (`CMD`/`ENTRYPOINT`).

- **Bygge:** `docker build -t mitimage:tag .` (punktum = kontekst, typisk nuværende mappe).
- **Køre:** `docker run mitimage:tag`. I Compose: `build: .` under en service – Compose bygger og bruger image ved `docker compose up --build`.

---

## Simpel Dockerfile (Node-app)

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3000
CMD ["node", "server.js"]
```

- **FROM** – base image (her Node 20 på Alpine Linux).
- **WORKDIR** – arbejdsmappe inde i containeren.
- **COPY** – kopiér filer fra build-kontekst (den mappe du kører `docker build` fra) ind i image.
- **RUN** – kør kommando ved *build* (her install af pakker).
- **EXPOSE** – dokumenterer at appen lytter på 3000; åbner ikke porten (det gør `-p` eller Compose `ports:`).
- **CMD** – standard kommando når containeren startes.

---

## .dockerignore

Opret en `.dockerignore` i samme mappe som Dockerfile (samme idé som .gitignore). Filer og mapper der matcher, kopieres *ikke* med til build-konteksten – hurtigere build og mindre image.

Eksempel:
```
node_modules
.git
.env
*.md
```

---

## Multi-stage build (avanceret)

Når I bygger kode (fx TypeScript eller Go), kan I bruge ét stage til at bygge og et andet til at køre – så det endelige image ikke indeholder build-værktøjer.

```dockerfile
# Stage 1: build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: run
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY --from=builder /app/dist ./dist
CMD ["node", "dist/server.js"]
```

Kun indholdet fra det sidste stage ender i det færdige image.

---

## Image vs. container (genopfriskning)

- **Build** skaber et **image** (lagret lokalt eller push til registry).
- **Run** starter en **container** fra det image. Ændringer i containeren ændrer ikke image – brug Dockerfile (eller `docker commit` sjældent) for at lave nye images.

Se [[Docker-grundlæggende#Image vs. container]].
