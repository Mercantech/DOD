---
tags:
  - dod
  - cicd
  - cicd/dokploy
---

# Dokploy – GitHub og webhooks

> **Dybere end dagens teori:** Forbinde repo, PAT/Deploy Key og webhook så push udløser deploy. Dag-note: [[../Noter/DoD - Pensum/Dag-08-Dokploy-og-GitHub]]. Install: [[Dokploy-installation-og-setup]]. Build: [[Dokploy-build-og-deploy]].

---

## Forbinde et GitHub-repository

1. **Opret projekt/app i Dokploy** – "New Project" eller "New Application", vælg typen (fx "Docker" eller "Docker Compose").
2. **Tilføj Git-kilde** – Angiv GitHub-repository (URL eller `owner/repo`).
   - **Offentligt repo:** Ofte ingen ekstra konfiguration.
   - **Privat repo:** Brug **Personal Access Token (PAT)** eller **Deploy Key** (SSH). PAT: GitHub → Settings → Developer settings → Personal access tokens, scope fx `repo`. Deploy Key: repo → Settings → Deploy keys.
3. **Vælg branch** – Fx `main`, så Dokploy bygger og deployer fra den branch.
4. **Build-konfiguration** – Angiv hvor Dockerfile eller `docker-compose.yml` ligger (typisk rod), og evt. build-argumenter eller environment variables til serveren.

Dokploy kan nu **manuelt** bygge og deploye. For **automatisk** deploy ved hvert push sættes en **webhook** op.

---

## Opsætte webhook (GitHub → Dokploy)

En **webhook** er en HTTP-anmodning GitHub sender til en URL når der sker noget i repo’et (fx push til `main`). Dokploy lytter og starter byg + deploy.

### I Dokploy

- Under app/projekt: find **"Webhook"**-sektionen med en URL, fx `https://dokploy.jeresdomæne.dk/api/webhook/...` (med token).
- Kopiér den fulde webhook-URL.

### I GitHub

1. Repository → **Settings** → **Webhooks** → **Add webhook**.
2. **Payload URL:** Indsæt Dokploy’s webhook-URL.
3. **Content type:** Ofte `application/json`.
4. **Trigger:** "Just the push event" (eller som anvist) så kun push til den valgte branch udløser deployment.
5. **Secret (valgfrit):** Hvis Dokploy understøtter det, kan I sætte fælles secret. Gem webhook.

Efter det vil **push til den valgte branch** sende en request til Dokploy, som bygger og deployer. Det er kernen i **CD** i jeres setup.
