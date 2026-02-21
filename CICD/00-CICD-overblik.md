---
tags:
  - dod
  - cicd
---

# CI/CD – pensum og overblik

Dette er **CI/CD-pensum** til DoD-kurset. Mappen bruges sammen med [[../Noter/DoD - Pensum/Program]] og dag-noterne. Her finder I dybdegående teori om **GitHub Actions** (CI), **Dokploy** (CD) og automatiseret deployment – mere end I når på Dag 8, 9 og 10.

> **Vil I dybere end hvad I når på en enkelt dag?** Hele denne mappe er **ekstra pensum** I kan dykke ned i. Start i dag-noterne; brug CICD-mappen når I vil forstå pipelines, webhooks og deployment i detaljer.

---

## Indhold i denne mappe

| Note | Indhold | Relevant for |
|------|---------|--------------|
| **[[CI-og-CD-koncepter]]** | CI vs. CD, pipeline som gate, tests før merge | Dag 8, hele uge 25 |
| **[[GitHub-Actions-grundlæggende]]** | Workflows, triggers, jobs, steps, branch protection, eksempel-pipeline | CI-delen af kurset |
| **[[GitHub-Actions-avanceret]]** | Caching, matrix, secrets, environments, prissætning, self-hosted runners | Når I udvider jeres pipeline |
| **[[Dokploy-overblik]]** | Hvad er Dokploy, self-hosted PaaS, CI vs. CD i kurset | **Dag 8** |
| **[[Dokploy-installation-og-setup]]** | Install på server, første adgang, konfiguration | Dag 8 |
| **[[Dokploy-GitHub-og-webhooks]]** | Forbinde repo, PAT/Deploy Key, webhook fra GitHub til Dokploy | **Dag 8** |
| **[[Dokploy-build-og-deploy]]** | Dockerfile vs. Compose i Dokploy, env vars, build-logs, typiske fejl | Dag 8, 9 |
| **[[Dokploy-volumes-og-monitoring]]** | Volumes i Dokploy, persistence, logs og monitoring | Dag 9, **Dag 10** |
| **[[Deployment-automatisering-praksis]]** | Hele flowet push → CI → CD, rollback, best practices | Dag 8–10, aflevering |

---

## Sådan hænger det sammen med kurset

- **Uge 25, Dag 8:** Dokploy op og GitHub på – brug [[Dokploy-overblik]], [[Dokploy-installation-og-setup]], [[Dokploy-GitHub-og-webhooks]]. Dag-note: [[../Noter/DoD - Pensum/Dag-08-Dokploy-og-GitHub]].
- **Uge 25, Dag 9:** Volumes og persistence i Dokploy – brug [[Dokploy-volumes-og-monitoring]] og [[../docker/Volumes-og-data]]. Dag-note: [[../Noter/DoD - Pensum/Dag-09-Volumes-Dokploy-og-Kubernetes]].
- **Uge 25, Dag 10:** Monitoring og logs – brug [[Dokploy-volumes-og-monitoring]] og Dag-note [[../Noter/DoD - Pensum/Dag-10-Monitoring-og-Logging]].
- **CI (GitHub Actions):** Hvis I sætter test-pipeline op – brug [[CI-og-CD-koncepter]], [[GitHub-Actions-grundlæggende]]. Samlet note i Noter: [[../Noter/CICD og GitHubActions]].

**Kort:** Dag-noterne giver overblik og læringsmål; CICD-mappen her giver **dybde** til dem der vil læse og fejlsøge videre.
