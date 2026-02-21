---
tags:
  - dod
  - cicd
  - cicd/github-actions
---

# GitHub Actions – grundlæggende

> **Dybere end dagens teori:** Workflows, triggers, jobs og steps – brug denne note når I sætter CI op med GitHub Actions. Dag-noter: [[../Noter/DoD - Pensum/Dag-08-Dokploy-og-GitHub]]. Samlet: [[../Noter/CICD og GitHubActions]]. Koncepter: [[CI-og-CD-koncepter]].

---

## Hvad er en workflow?

En **workflow** er en automatiseret proces defineret i en YAML-fil under `.github/workflows/`. Den kan køre ved fx push, pull_request eller schedule.

- **Trigger (`on`):** Hvornår kører workflow’en? Fx `push`, `pull_request`, `workflow_dispatch`.
- **Jobs:** En eller flere jobs; hvert job kører på en runner (fx `ubuntu-latest`).
- **Steps:** Inden for et job – checkout, setup, build, test. Et step fejler → jobbet fejler → workflow fejler.

---

## Simpel pipeline – eksempel

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

- **on:** Kør ved PR og ved push til `main`.
- **runs-on: ubuntu-latest:** GitHub-hosted Linux-runner.
- **uses:** Genbrugelige actions (checkout, setup-dotnet).
- **run:** Egne shell-kommandoer. Hvis én fejler, stopper jobbet.

Essensen af **CI:** Koden skal bygge, tests skal være grønne; pipeline stopper hvis noget fejler.

---

## Branch protection og "Required status checks"

For at **tvinge** at CI er grøn før merge:

1. Repository **Settings** → **Branches** → **Branch protection rules** for `main`.
2. Aktiver **"Require status checks to pass before merging"**.
3. Vælg de jobs der skal være grønne (fx "build-and-test" eller de navne I giver jeres jobs).

Så blokerer GitHub merge indtil de valgte checks er grønne. Det er her CI virkelig fungerer som **gate**.

---

## Secrets og miljø

- **API-nøgler, passwords, connection strings** må **ikke** committes. Brug **GitHub Secrets** (Settings → Secrets and variables → Actions).
- I workflow: `env: MY_SECRET: ${{ secrets.MY_SECRET }}`. Secrets vises ikke i logs; GitHub redacter dem.
- Til test-compose i CI bruger I typisk **kun demo-værdier**. Produktion håndteres af Dokploy og .env på serveren.

Se [[GitHub-Actions-avanceret]] for caching, matrix og self-hosted runners.
