---
tags:
  - dod
  - cicd
---

# Deployment-automatisering – praksis

> **Dybere end dagens teori:** Hele flowet fra push til live, rollback og best practices. Dag-noter: [[../Noter/DoD - Pensum/Dag-08-Dokploy-og-GitHub]], [[../Noter/DoD - Pensum/Dag-10-Monitoring-og-Logging]]. Koncepter: [[CI-og-CD-koncepter]].

---

## Hele flowet: push → CI → CD

1. **Udvikler pusher** (eller merger PR til `main`).
2. **CI (GitHub Actions):** Hvis I har sat workflow op – build og test kører. Ved fejl stopper pipelinen; merge blokerer hvis branch protection er slået til.
3. **CD (Dokploy):** Ved push til `main` sender GitHub webhook til Dokploy. Dokploy henter kode, bygger image/compose og deployer. Appen opdateres på serveren.

**Uden CI:** Kode kan merges og deployes uden at tests er kørt. **Med CI:** Kun godkendt kode kan merges og dermed blive deployet af Dokploy.

---

## Rollback og fejlsøgning

- **Rollback:** I Dokploy kan I typisk deploye en **tidligere version** (tidligere image eller tidligere commit) – tjek Dokploy’s UI for deploy-historik og "Redeploy" eller lign. Alternativt: revert commit og push igen, så webhook udløser ny deploy med gammel kode.
- **Fejlsøgning:** Brug **build-logs** (hvor fejlede build?) og **runtime-logs** (hvorfor crasher containeren?). Se [[Dokploy-build-og-deploy]] og [[Dokploy-volumes-og-monitoring]].

---

## Best practices (kort)

- **CI før CD:** Sørg for at tests kører (GitHub Actions) og at merge til main kræver grøn CI (branch protection).
- **Secrets:** Ingen passwords eller API-nøgler i kode – brug GitHub Secrets til CI og Dokploy/env vars til produktion.
- **Volumes:** Database og anden persisteret data i volumes, så de overlever redeploy. Se [[Dokploy-volumes-og-monitoring]].
- **Dokumentation:** Notér jeres flow (push → webhook → Dokploy) og hvordan I ruller tilbage – det er en del af afleveringskrav på [[../Noter/DoD - Pensum/Dag-15-Aflevering]].
