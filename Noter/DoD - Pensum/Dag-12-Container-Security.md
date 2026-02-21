---
tags:
  - dod
  - sikkerhed
---

# Dag 12 – Container Security & Secrets Management

> Teori til Dag 12 (23. juni). I dag sikrer I *jeres* containere og hemmeligheder – best practices, env vs. secrets, og scanning for sårbarheder. Se [[Program]] for dagens mål og plan. **Dybere teori:** [[../../Sikkerhed/00-Sikkerhed-overblik]]. **Bygger på:** [[Dag-11-OWASP-og-sikkerhed]] (sikker kode og OWASP). **Relateret:** [[Dag-13-CTF]] (praktisk sikkerhedstestning).

---

## Docker-sikkerhed – best practices

Sikkerhed for **containere** handler om at begrænse hvad en container kan gøre og hvad den har adgang til – så et kompromitteret app eller image giver mindst mulig skade.

### Kør ikke som root

Containere kører som **root** inde i containeren som standard. Hvis angriberen bryder ind i appen, har de root-rettigheder i containerens filsystem og processer. **Løsning:** Opret en ikke-root-bruger i Dockerfile og kør appen som den.

**Eksempel (Dockerfile):**
```dockerfile
FROM node:20-alpine
RUN addgroup -g 1001 appgroup && adduser -u 1001 -G appgroup appuser
WORKDIR /app
COPY --chown=appuser:appgroup . .
USER appuser
CMD ["node", "server.js"]
```

- `USER appuser` sikrer at CMD kører som `appuser`, ikke root.

### Minimal base image og få lag

- Brug **slim** eller **alpine**-images hvor det giver mening – færre pakker = færre potentielle sårbarheder og mindre angrebsflade.
- Hold Dockerfile **ren**: kun nødvendige COPY og RUN. Unødvendige værktøjer (curl, shell) kan misbruges hvis nogen får adgang.

### Read-only og begrænsede rettigheder

- **Read-only filsystem:** `docker run --read-only ...` – containeren kan ikke skrive til filsystemet (undtagen evt. tmpfs eller eksplicitte mounts). For mange apps kræver det at temp/log skrives til et volume.
- **Begræns capabilities:** Docker giver som standard en del Linux capabilities. I høj-sikkerhedsmiljøer kan I fjerne dem med `--cap-drop=ALL` og kun tillade det I har brug for.

### Netværk

- Eksponér kun de **porte** appen virkelig skal have. Undlad at mappe interne porte ud mod hosten hvis ingen har brug for det.
- Brug **brugerdefinerede netværk** (fx Docker Compose-netværk) i stedet for default bridge, så I bedre kan styre hvem der taler med hvem.

### Images: hvad kommer ind?

- **Byg selv** fra en Dockerfile med kendt base – så ved I hvad der er i. Hold base og afhængigheder **opdateret**.
- **Scan** images for kendte sårbarheder (Trivy, Snyk) – se nedenfor. Det dækker OWASP A06 (Vulnerable and Outdated Components).

---

## Environment variables vs. secrets

Begge bruges til konfiguration (fx database-URL, API-nøgler). Forskellen er **hvor følsomme** data er og **hvordan** de håndteres.

### Environment variables

- Sættes med `-e` ved `docker run` eller `environment:` i Compose.
- **Synlige** i `docker inspect` og i process-listen på hosten (`/proc`). Enhver med adgang til at liste containere eller processer kan læse dem.
- **Godt til:** ikke-følsomme indstillinger (fx `NODE_ENV=production`, `LOG_LEVEL=info`, database-*host* uden password).

### Secrets

- **Secrets** er følsomme data (passwords, API-nøgler, private keys) der ikke bør stå som almindelige env vars. De kan leveres som **filer** der mountes read-only ind i containeren (så appen læser fra fil i stedet for env), eller via **Docker Secrets** (Swarm) / **Kubernetes Secrets** / tjenester som HashiCorp Vault.
- **Docker Compose** (standalone): Der findes ikke "Docker Secrets" som i Swarm, så I bruger typisk **env filer** der ikke committes (`.env` i `.gitignore`) og læses med `env_file:`, eller I mounter en fil med hemmeligheden fra et sikkert sted. Vigtigt: **kom aldrig** credentials med i image eller i Git.
- **Princip:** Jo mere følsomt, jo tættere på "secret"-håndtering (fil med begrænset læsning, eller dedikeret secrets-backend). Environment variables er **praktiske** men ikke sikre mod at blive lækket ved inspect eller fejllogning.

### Kort sammenfatning

| | Environment variables | Secrets (fx fil / secrets-backend) |
|--|------------------------|-------------------------------------|
| **Brug til** | Ikke-følsom konfiguration | Passwords, API-nøgler, certifikater |
| **Synlighed** | Synlige i inspect/process | Læses som fil eller injiceret sikkert |
| **I Compose** | `environment:` eller `env_file:` | `.env` uden for Git, eller fil-mount |
| **I produktion** | Opsætning, feature flags | Credentials fra vault eller CI-secrets |

---

## Container scanning – Trivy og Snyk

**Container scanning** tjekker et **image** (lag for lag) mod databaser med kendte sårbarheder (CVEs). Det hjælper med OWASP A06 (Vulnerable and Outdated Components): at I ikke deployer images med kendte huller.

### Trivy

- **Trivy** er open source og kan køre lokalt mod et image uden login.
- **Installation:** Download fra [github.com/aquasecurity/trivy](https://github.com/aquasecurity/trivy) eller `apt install trivy` / brew.
- **Scan et image:**  
  `trivy image <image:tag>`  
  fx `trivy image node:20-alpine` eller `trivy image minapp:latest`
- Output viser **sårbarheder** (CVE-id, alvorlighed, pakke, fix-version). I kan rette ved at opdatere base image eller afhængigheder og bygge igen.

**Eksempel (kort):**
```bash
trivy image myapp:latest
```
- **Severity:** CRITICAL, HIGH, MEDIUM, LOW. Prioriter at lukke CRITICAL og HIGH før produktion.
- Trivy kan også scanne **filer** (Dockerfile, docker-compose) for misconfiguration.

### Snyk

- **Snyk** tilbyder container scanning (og scanning af kode/afhængigheder). Kræver typisk konto og CLI-login (`snyk auth`).
- **Scan:**  
  `snyk container test <image:tag>`  
  eller integration i CI/CD (GitHub Actions, etc.).
- Snyk giver også **remediation** (opdateringsforslag) og kan overvåge projekter over tid.

**Praktisk:** Start med **Trivy** for hurtig, lokal scanning uden konto. Brug Snyk hvis I allerede har det i pipeline eller vil have integration til issues og fix-forslag.

### Efter scanning

- **Opdater** base image (fx `node:20-alpine` → nyere patch) og afhængigheder i appen (`npm update`, `pip install -U`).
- **Genbyg** image og **scan igen** indtil I er tilfredse med niveau (fx ingen CRITICAL/HIGH).
- Gør scanning til en del af **CI** (fx ved push eller før deploy), så nye sårbarheder ikke ryger i produktion.

---

## Læringsmål (opsummering)

1. Gennemgå sikkerheds-praksis for Docker-containere: kør ikke som root, minimal image, read-only hvor muligt, begrænset netværk; kendskab til brugere, netværk og images.
2. Forklare forskellen på environment variables og secrets – env til ikke-følsom konfiguration (synlig i inspect); secrets til passwords og nøgler (fil eller secrets-backend). Hvornår man bruger hvad.
3. Scanne et Docker-image for kendte sårbarheder med fx Trivy eller Snyk – køre scan, læse resultater (CVE, severity), og handle (opdatere, genbygge, gen-scanne).

---

## Videre læsning

- **Dag 11** ([[Dag-11-OWASP-og-sikkerhed]]) – OWASP Top 10 og sikker kode (A06: uddaterede komponenter).
- **Dag 13** ([[Dag-13-CTF]]) – praktisk sikkerhedstestning; scanning supplerer med at finde sårbarheder i koden.
