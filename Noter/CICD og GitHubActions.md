---
tags:
  - dod
  - cicd
  - cicd/github-actions
---

**Dybere pensum i CICD-mappen:** [[../CICD/00-CICD-overblik]] – GitHub Actions, Dokploy, webhooks og deployment-automatisering.

## **CI/CD – hvad er det helt præcist?**


![[Pasted image 20260221162551.png]]

### **Continuous Integration (CI)**

CI handler om at teste og validere koden **før** den rammer en vigtig branch (fx `main`, `dev`, `staging`).

**CI** sørger for:

- Bygger projektet
- Kører unit- og integrationstests
- Checker PRs
- Stopper dårlig kode **tidligt**
- Giver udvikleren feedback i GitHub

<aside>
🧠

CI = *“Er koden god nok til at komme i main?”*

</aside>

### **Continuous Deployment (CD)**

**CD** handler om *hvad der sker efter koden er godkendt, altså efter **CI***

Typisk:

- Bygge Docker-image
- Deploye til staging/production
- Starte containere og services

I vores opsætning håndteres CD af **Dokploy**, ikke GitHub.

<aside>
🧠

CD = *“Deploy den nye version – når den er testet og klar.”*

</aside>

---

## **Hvor passer tests ind i pipelinen?**

En professionel pipeline bruger tests som “gates”:

**1. CI (GitHub Actions)**

Kør tests FØR merge:

- Build
- Unit tests
- Integration tests
- Bruno E2E via docker-compose test-miljø
- lint og basic quality checks

**Kun hvis CI er grønt → må koden merges til `main`.**

**2. CD (Dokploy)**

Efter merge:

- Deploy til server
- Opdater containers
- Rollback hvis noget går galt

---

## **Eksempel på en simpel GitHub Actions pipeline (.NET + Bruno)**

Eleverne får dette som skabelon:

```yaml
name: CI Pipeline

on:
  pull_request:
  push:
    branches: ["main"]

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout kode
      uses: actions/checkout@v4

    - name: Setup .NET
      uses: actions/setup-dotnet@v4
      with:
        dotnet-version: 8.0.x

    - name: Build projekt
      run: dotnet build --configuration Release

    - name: Unit tests
      run: dotnet test --no-build --verbosity normal

    - name: E2E Tests (Bruno)
      run: |
        docker compose -f docker-compose.tests.yml up --abort-on-container-exit
```

Dette er essensen af **CI**:

- Koden skal bygge
- Tests skal være grønne
- E2E kan køres i et midlertidigt docker-compose setup
- Pipeline stopper hvis noget fejler og ingen kode kommer ind på vigtige branches

### Sådan ser vores egen pipeline ud https://github.com/Mercantech/h4-mags

I dette projekt er CI opdelt i to jobs:

1. **unit-tests** – Byg og kør Backend.Tests (.NET). Hvis det fejler, kører resten ikke.
2. **api-tests** – Start `docker-compose.test.yml` (PostgreSQL + Seq + Backend), vent på at API svarer, installer Bruno CLI, kør E2E-UserFlows mod `http://localhost:9080`, upload JUnit-rapport som artifact. Ved fejl logges backend/postgres; til sidst ryddes containere op.

Se den fulde workflow i https://github.com/Mercantech/H4-MAGS/blob/main/.github/workflows/ci.yml

- Her kan I se den komplette for Kahoot projektet, i dens nuværende stadie 18/02/26
    
    ```yaml
    services:
      backend:
        build:
          context: ./Backend
          dockerfile: API/Dockerfile
        ports:
          - "9080:5000"
        env_file:
          - .env
        environment:
          - ASPNETCORE_URLS=http://+:5000
          - ASPNETCORE_ENVIRONMENT=Production
          # Seq logging - bruger Docker service navn internt (http://seq:80)
          # For ekstern adgang, sæt Seq__ServerUrl=https://kahoot-log.mercantec.tech i .env filen
          - Storage__MinIO__Endpoint=http://minio:9000
          - Storage__MinIO__BucketName=kahoot-uploads
          - Storage__MinIO__AccessKey=${MINIO_ROOT_USER:-minioadmin}
          - Storage__MinIO__SecretKey=${MINIO_ROOT_PASSWORD:-minioadmin}
        depends_on:
          - seq
          - minio
        networks:
          - app-network
    
      flutterweb:
        build:
          context: ./flutter_app
          dockerfile: Dockerfile
          args:
            - BUILDKIT_INLINE_CACHE=1
        ports:
          - "9081:80"
        depends_on:
          - backend
        env_file:
          - .env
        networks:
          - app-network
    
      seq:
        image: datalust/seq:latest
        ports:
          - "9082:80"    # HTTP UI og API
          - "5341:5341"  # HTTPS (for ekstern adgang)
        environment:
          - ACCEPT_EULA=Y
          - SEQ_FIRSTRUN_ADMINPASSWORD=Admin123!
        volumes:
          - seq-data:/data
        restart: unless-stopped
        networks:
          - app-network
    
      # MinIO – S3-kompatibel objektlager med Web UI (kun prod, ikke i docker-compose.test.yml)
      minio:
        image: minio/minio:latest
        # Uden --console-address bruger MinIO en dynamisk port til Web UI (fx 37995); 9085:9001 virker kun med fast port.
        command: server --console-address ":9001" /data
        environment:
          MINIO_ROOT_USER: ${MINIO_ROOT_USER:-minioadmin}
          MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD:-minioadmin}
        ports:
          - "9084:9000"   # S3 API
          - "9085:9001"   # Web Console
        volumes:
          - minio-data:/data
        restart: unless-stopped
        networks:
          - app-network
    
      # Bruno – kør E2E-UserFlows én gang ved deploy (som H2), skriv HTML til delt volume. restart: no = engang-job.
      bruno-run-on-deploy:
        build:
          context: ./Bruno
          dockerfile: Dockerfile
        entrypoint: ["sh", "-c"]
        volumes:
          - ./Bruno:/collection
          - bruno-reports:/collection/reports
        environment:
          - API_BASE_URL=https://kahoot-api.mercantec.tech
        command: ["mkdir -p /collection/reports && echo 'Venter på API...' && sleep 15 && bru run E2E-UserFlows -r --sandbox=developer --env Kahoot --env-var \"baseUrl=$$API_BASE_URL\" --reporter-html /collection/reports/results.html && echo 'Rapport skrevet til bruno-reports volume'"]
        depends_on:
          - backend
        restart: "no"
        networks:
          - app-network
    
      # Bruno CLI – manuel kør (fx lokalt). Kør: docker compose --profile cli run bruno-cli
      bruno-cli:
        build:
          context: ./Bruno
          dockerfile: Dockerfile
        entrypoint: ["sh", "-c"]
        volumes:
          - ./Bruno:/collection
          - bruno-reports:/collection/reports
        environment:
          - API_BASE_URL=https://kahoot-api.mercantec.tech
        command: ["mkdir -p /collection/reports && bru run E2E-UserFlows -r --sandbox=developer --env Kahoot --env-var \"baseUrl=$$API_BASE_URL\" --reporter-html /collection/reports/results.html"]
        profiles:
          - cli
    
      # Server E2E-rapporten (uden profile – startes ved deploy). Fx https://kahoot-bruno.mercantec.tech
      # Opdateres automatisk ved deploy via bruno-run-on-deploy (som H2).
      bruno-reports:
        build:
          context: ./Bruno
          dockerfile: reports-Dockerfile
        ports:
          - "9083:80"
        volumes:
          - bruno-reports:/usr/share/nginx/html:ro
          - ./Bruno/reports-nginx.conf:/etc/nginx/conf.d/reports.conf:ro
        restart: unless-stopped
        networks:
          - app-network
    
    networks:
      app-network:
        driver: bridge
    
    volumes:
      seq-data:
      bruno-reports:
      minio-data:
    ```
    

---

## **GA vs. Dokploy – den korte forklaring**

| Funktion | GitHub Actions (CI) | Dokploy (CD) |
| --- | --- | --- |
| Tester ved PR | ✅ Ja | ❌ Nej |
| Stopper merge ved fejl | ✅ Ja | ❌ Nej |
| Tester i miljø | ⚠️ Kun hvis vi spinner docker op | ✅ Ja |
| Deploy | ❌ Nej | ✅ Ja |

**GitHub Actions = kvalitetssikring før merge.**

**Dokploy = deployment efter merge.**

Et andet eksempel på automatiseret deployment er **[[Proxi-demo]]**: der bruges Ansible-playbooks til at bygge image og deploye til et K3s-cluster (ingen GitHub webhook, men samme idé – deployment fra kode/kontroller).

## Branch protection og “Required status checks”

For at **tvinge** at CI er grøn før merge:

1. **Settings → Branches → Branch protection rules** for `main`.
2. Aktiver “Require status checks to pass before merging”.
3. Vælg fx “Unit tests” og “Bruno API tests (demo container)”.

Så blokerer GitHub merge indtil begge jobs er grønne. Det er her CI virkelig fungerer som gate.

---

## Secrets og miljø – hvad skal ikke ligge i koden

- **API-nøgler, passwords, connection strings** skal **ikke** committes. Brug **GitHub Secrets** (Settings → Secrets and variables → Actions).
- I workflow kan I bruge dem som: `env: MY_SECRET: ${{ secrets.MY_SECRET }}`.
- I vores test-compose bruger vi **ingen** rigtige secrets: JWT og DB er demo-værdier kun til CI. Produktion håndteres af Dokploy og .env på serveren.

**Husk:** Secrets vises ikke i logs; GitHub redacter dem automatisk.

---

## Det er værd at vide mere om (når I vil gå videre)

- **Caching** – `actions/cache` til NuGet eller npm gør andre runs hurtigere.
- **Matrix** – Kør samme job på flere .NET-versioner eller OS med `strategy.matrix`.
- **Scheduled runs** – `on: schedule:` med cron (fx natlige tests) for at fange flaky eller miljø-problemer.
- **Miljøer (environments)** – GitHub “environments” med approval eller secrets per miljø (staging vs prod).
- **Officiel dokumentation** – [GitHub Actions docs](https://docs.github.com/en/actions) og [Workflow syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions).

## Prissætning – minutter og hvornår det koster

### Hvad koster GitHub Actions?

- **Offentlige (public) repos:** Brug af standard GitHub-hostede runners er **gratis** – ubegrænset antal minutter.
- **Private repos:** Du får et **kvote af gratis minutter** pr. måned efter din plan. Minutter nulstilles ved start af hver faktureringsperiode. Alt over kvoten bliver faktureret (eller blokeret, hvis der ikke er betalingsmetode).

Så for skole-/hobbyprojekter med public repo betaler I typisk **0 kr.** for CI. Da vi altid bruger public repos, på en org, har vi aldrig ramt en mur! 

### Hvad er “minutter”?

GitHub måler **forbrug per minut**, mens et job kører på en **runner** (en virtuel maskine). Regningen afhænger af:

- **Hvor længe** jobbet kører (1 job i 10 min = 10 minutter forbrug).
- **Hvilken runner-type** I bruger:
    - **Linux** (fx `ubuntu-latest`) er billigst – standard 2-core koster ca. $0,006/min.
    - **Windows** er dyrere (ca. $0,010/min).
    - **macOS** er væsentligt dyrere (ca. $0,062/min).

Vores CI bruger `runs-on: ubuntu-latest`, så vi trækker kun Linux-minutter – det holder forbruget nede.

**Eksempel:** 100 CI-runs á 5 min på Linux = 500 minutter. På GitHub Free (2.000 inkl. min/md) er det under kvoten. På en betalt plan vil overskydende minutter blive faktureret til den angivne per-minut pris.

### Gratis minutter per plan (pr. måned, private repos)

| Plan | Inkl. minutter/md | Artifact-lagring |
| --- | --- | --- |
| GitHub Free | 2.000 | 500 MB |
| GitHub Pro | 3.000 | 1 GB |
| GitHub Team | 3.000 | 2 GB |
| GitHub Enterprise Cloud | 50.000 | 50 GB |

Kilde: [GitHub Actions billing](https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions). Større/luxury-runners (fx flere kerner) koster altid ekstra, også for public repos.

### Self-hosted runners som alternativ

I stedet for GitHub’s egne maskiner kan I køre jobs på **jeres egen maskine** – en **self-hosted runner**.

- **Fordele:**
    - **Ingen minut-regning** fra GitHub for selve runner-tiden (GitHub tæller ikke disse minutter mod jeres kvote).
    - God til tunge eller specialiserede miljøer (bestemt .NET-version, Docker-in-Docker, adgang til internt netværk).
    - Hurtigere runs hvis maskinen er kraftig og allerede har cache.
- **Ulemper:**
    - I skal selv vedligeholde maskinen (opdateringer, sikkerhed, oppetid).
    - Runneren må være tilgængelig når workflows kører (fx en VM eller en dedikeret PC).
    - **Sikkerhed:** En kompromitteret repo kan køre kode på jeres runner; brug derfor kun til repos I stoler på, eller brug isolerede/efemære runners.

**Opsummering:** Til almindelig CI (build + test) er GitHub-hosted Linux ofte det enkleste og billigste. Self-hosted giver mening når I har behov for særligt miljø eller vil undgå minut-forbrug på private repos.