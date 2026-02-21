---
tags:
  - dod
  - sikkerhed
  - sikkerhed/container
---

# Container-sikkerhed

> **Dybere end dagens teori:** Non-root, minimal image, env vs. secrets, Trivy/Snyk. Dag-note: [[../Noter/DoD - Pensum/Dag-12-Container-Security]]. OWASP A06: [[OWASP-Top-10-dybde]].

---

## Kør ikke som root

Containere kører som **root** inde i containeren som standard. **Løsning:** Opret ikke-root-bruger i Dockerfile og kør appen som den.

```dockerfile
FROM node:20-alpine
RUN addgroup -g 1001 appgroup && adduser -u 1001 -G appgroup appuser
WORKDIR /app
COPY --chown=appuser:appgroup . .
USER appuser
CMD ["node", "server.js"]
```

---

## Minimal base image og få lag

- Brug **alpine** eller **slim**-images – færre pakker = mindre angrebsflade.
- Hold Dockerfile ren: kun nødvendige COPY og RUN. Unødvendige værktøjer kan misbruges.

---

## Environment variables vs. secrets

| | Environment variables | Secrets (fil / backend) |
|--|------------------------|--------------------------|
| **Brug til** | Ikke-følsom konfiguration | Passwords, API-nøgler |
| **Synlighed** | Synlige i `docker inspect` og process-liste | Læses fra fil eller injiceret sikkert |
| **I Compose** | `environment:` eller `env_file:` | `.env` uden for Git, eller fil-mount |

**Princip:** Credentials og API-nøgler bør ikke stå som almindelige env vars; brug fil eller secrets-backend. Kom aldrig credentials med i image eller Git.

---

## Container scanning – Trivy og Snyk

**Trivy** (open source, lokalt uden login):
```bash
trivy image minapp:latest
```
Viser CVE, alvorlighed, pakke og fix-version. Opdater base og afhængigheder, genbyg og scan igen. Prioriter CRITICAL og HIGH.

**Snyk:** Kræver konto; giver remediation og integration i CI/CD.

Gør scanning til en del af **CI** (fx GitHub Actions), så nye sårbarheder ikke ryger i produktion. Det dækker OWASP A06 (Vulnerable and Outdated Components).
