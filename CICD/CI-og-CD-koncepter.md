---
tags:
  - dod
  - cicd
  - cicd/github-actions
---

# CI og CD – koncepter

> **Dybere end dagens teori:** Denne note forklarer CI og CD som idéer – brug den sammen med [[../Noter/DoD - Pensum/Dag-08-Dokploy-og-GitHub]] og [[GitHub-Actions-grundlæggende]]. Samlet gennemgang findes også i [[../Noter/CICD og GitHubActions]].

---

## Hvad er Continuous Integration (CI)?

**CI** handler om at **teste og validere koden automatisk**, typisk **før** den rammer en vigtig branch (fx `main` eller `master`).

- Bygge projektet
- Køre unit- og integrationstests
- Lint og kvalitetstjek
- Ved **pull request**: kun tillade merge når CI er grøn

**Idéen:** Dårlig kode blokerer tidligt; udvikleren får feedback i GitHub uden at manuelt køre tests hver gang. I kurset bruges **GitHub Actions** til CI.

**Kort:** *"Er koden god nok til at komme i main?"*

---

## Hvad er Continuous Deployment (CD)?

**CD** handler om **hvad der sker efter** koden er godkendt – altså efter CI (eller efter manuelt merge).

- Bygge Docker-image (hvis det sker på serveren)
- Deploye til server / staging / production
- Starte eller opdatere containere og services

I DoD-kurset håndteres **CD af Dokploy**: push til `main` → webhook → Dokploy bygger og deployer. GitHub Actions bruges til **CI** (tests), ikke til selve deployment.

**Kort:** *"Deploy den nye version – når den er testet og klar."*

---

## Pipeline som "gate"

En typisk pipeline bruger **tests som gate**:

| Trin | Hvor | Hvad sker der |
|------|------|----------------|
| **1. CI (GitHub Actions)** | Ved PR eller push til `main` | Build, unit tests, evt. E2E (fx Bruno i Docker). Hvis noget fejler, stopper pipelinen. |
| **2. Merge** | Kun hvis CI er grøn | Kode merges til `main`. Branch protection kan **tvinge** at CI er grøn før merge. |
| **3. CD (Dokploy)** | Ved push til `main` | Webhook udløser Dokploy → build → deploy. Appen opdateres på serveren. |

**Vigtigt:** CI sikrer kvalitet **før** merge; CD sørger for at den godkendte kode **kommer live**. Uden CI kan dårlig kode ryge ind i `main` og derefter blive deployet af Dokploy.

---

## GA vs. Dokploy – den korte forklaring

| Funktion | GitHub Actions (CI) | Dokploy (CD) |
|----------|---------------------|--------------|
| Tester ved PR | ✅ Ja | ❌ Nej |
| Stopper merge ved fejl | ✅ Ja | ❌ Nej |
| Deploy til server | ❌ Nej | ✅ Ja |
| Kører på jeres server | ❌ (eller self-hosted) | ✅ Ja |

Se [[Dokploy-overblik]] og [[Deployment-automatisering-praksis]] for hele flowet.
