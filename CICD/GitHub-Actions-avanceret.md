---
tags:
  - dod
  - cicd
  - cicd/github-actions
---

# GitHub Actions – avanceret

> **Dybere end dagens teori:** Caching, matrix, prissætning og self-hosted runners. Bygger på [[GitHub-Actions-grundlæggende]]. Samlet note: [[../Noter/CICD og GitHubActions]].

---

## Caching

`actions/cache` gør gentagne runs hurtigere ved at gemme fx NuGet- eller npm-cache mellem kørsler.

- Nøgle: ofte baseret på lock-fil (fx `hashFiles('**/package-lock.json')`).
- Restore og save paths: hvor cachen ligger (fx `~/.nuget/packages`, `node_modules`).

Kortere build-tid og mindre download ved hver run.

---

## Matrix

Kør samme job på **flere versioner eller OS** med `strategy.matrix`:

```yaml
strategy:
  matrix:
    dotnet-version: ['6.0', '8.0']
    os: [ubuntu-latest, windows-latest]
```

Så kører jobbet for hver kombination (her 2×2 = 4 runs). Nyttigt til at teste på flere .NET-versioner eller platforme.

---

## Scheduled runs og environments

- **on: schedule:** Cron-udtryk (fx `0 2 * * *` for natlige runs) – fanger flaky tests eller miljø-problemer.
- **Environments:** GitHub "environments" (fx staging, production) med egne secrets eller **approval** før deploy. Mere relevant når I bruger GA til deployment; i DoD håndteres deploy af Dokploy.

---

## Prissætning – minutter

- **Public repos:** Standard GitHub-hosted runners er **gratis** – ubegrænsede minutter.
- **Private repos:** Gratis kvote pr. måned (fx 2.000 min for GitHub Free); derefter fakturering.
- **Runner-type:** Linux billigst, Windows dyrere, macOS væsentligt dyrere. Hold jer til `ubuntu-latest` for at holde forbruget nede.

Kilde: [GitHub Actions billing](https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions).

---

## Self-hosted runners

I stedet for GitHub’s maskiner kan I køre jobs på **jeres egen maskine** (self-hosted runner).

- **Fordele:** Ingen minut-regning for runner-tiden; specialmiljø (bestemt .NET, Docker-in-Docker); hurtigere hvis maskinen har cache.
- **Ulemper:** I vedligeholder maskinen; den skal være tilgængelig når workflows kører; **sikkerhed** – kompromitteret repo kan køre kode på runneren.

Brug til repos I stoler på, eller isolerede/efemære runners. Til almindelig CI er GitHub-hosted Linux ofte enklest.
