---
tags:
  - dod
  - cicd
---

# Proxi – demo på infrastruktur og K3s

> **Proxi** er kursets demo på **infrastruktur som kode** og **konfiguration som kode**: Terraform, Ansible og Kubernetes (K3s) bruges til at sætte et lille cluster op med Postgres og en Node-app. Denne note binder Proxi-demoen sammen med resten af kurset.

---

## Hvor passer Proxi ind i kurset?

- **[[Program]]** – Dag 9 (Volumes, Dokploy, Kubernetes) bruger Proxi som eksempel på K3s, volumes og deployment.
- **[[Dag-09-Volumes-Dokploy-og-Kubernetes]]** – Teori om Docker volumes, PVC og K8s-ressourcer med konkrete eksempler fra Proxi (namespace, Deployment, Service, Ingress).
- **[[Dag-06-Docker-grundlæggende]]** og **[[Dag-07-Docker-Compose]]** – Proxi bruger Docker til at *bygge* app-image og Docker Compose til lokal/alternativ kørsel; selve produktion kører i K3s.
- **[[Dag-03-Database-Setup-med-Docker]]** – Samme idé: database i container; i Proxi kører Postgres i K3s med PVC.
- **[[CICD og GitHubActions]]** – I kurset håndteres CD ofte med Dokploy (Git push → deploy). Proxi viser et andet flow: **Ansible-playbooks** der bygger image og deployer til K3s (deploy-k8s.yml) – samme tanke: automatiseret deployment fra kode.

---

## Proxi-dokumentation (i repoet)

Proxi-repoet har en **docs/**-mappe med reference og koncepter. Brug dem sammen med dagens teori:

| Note | Indhold |
|------|---------|
| **[[Koncepter-og-overblik]]** | Hvad er Proxi, Terraform, Ansible, K3s, K8s-ressourcer (Namespace, Secret, PVC, Deployment, Service, Ingress), Docker. Kort deploy-flow. |
| **[[K3s-og-Postgres]]** | Nuværende setup (Docker på VM’er, Postgres på control plane, nginx load balancer) og hvordan det bliver til K3s (Deployment, Service, Ingress, PVC). |
| **[[Deploy-og-rollout]]** | Trin for trin: hvad sker der når du kører `deploy-k8s.yml`, kun app ændret vs. kun K8s ændret, hurtig genstart af pods. |

Den levende version med diagrammer er forsiden på Proxi-appen (fx http://10.133.51.120 eller via SSH-tunnel).

---

## Kort overblik over Proxi

- **Terraform** → opretter 3 VM’er (1 control plane, 2 workers) på Proxmox.
- **Ansible** → installerer K3s, bygger app-image, deployer med `kubectl apply`, rollout restart.
- **K3s** → namespace `proxi`, Postgres med PVC, app med 3 replicas, Services (`proxi-db`, `proxi-app`), Traefik Ingress.
- **Docker** → bruges til at bygge `proxi-demo:latest`; kørsel sker i K3s (containerd).

Se **[[Koncepter-og-overblik]]** og **[[Dag-09-Volumes-Dokploy-og-Kubernetes]]** for detaljer.
