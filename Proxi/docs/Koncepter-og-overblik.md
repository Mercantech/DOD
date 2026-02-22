# Koncepter og overblik – Proxi

Denne fil er en reference til de koncepter og værktøjer vi bruger i Proxi. Den levende version med diagrammer er forsiden på appen (http://10.133.51.120 eller via SSH-tunnel).

---

## Hvad er Proxi?

Proxi er et lille, komplet eksempel på **infrastruktur som kode** og **konfiguration som kode**. VM’er og software oprettes/konfigureres ud fra filer (Terraform, Ansible, Kubernetes YAML) – ikke manuelt. Resultatet: et 3-nodes K3s-cluster med Postgres og en demo-app på Proxmox.

---

## Terraform & Proxmox

- **Terraform** – Læser HCL-filer og taler med en *provider* (her Proxmox) for at oprette/opdatere/slette ressourcer. Du beskriver ønsket tilstand; Terraform udfører.
- **Proxmox VE** – Virtualiseringsplatform med UI og API. Terraform bruger API’en til at styre VM’er.
- **I Proxi** – Terraform kloner en Ubuntu-template tre gange (1 control plane, 2 workers), med statisk IP, diskstørrelse, cloud-init (bruger, SSH-nøgler, netværk).

---

## Ansible

- **Ansible** – Konfigurationsværktøj. Forbinder via SSH og kører *tasks* fra YAML-playbooks. Bruger et *inventory* (liste af hosts med IP’er).
- **Playbooks og inventory** – Inventory = hvilke maskiner; playbook = hvilke tasks på hvilke hosts. Idempotent: kør igen uden at ødelægge.
- **I Proxi** – **k3s.yml**: installerer K3s server/agent, iptables, disk-tjek. **deploy-k8s.yml**: bygger app-image, distribuerer til noder, `kubectl apply`, rollout restart.

---

## K3s & Kubernetes

- **Kubernetes** – Platform til containere: du beskriver app og adgang i YAML; K8s starter pods, genstarter ved fejl, distribuerer trafik.
- **K3s** – Letvægts-Kubernetes: én binær med API server, kubelet, containerd, Traefik, flannel. Server på CP, agent på workers.
- **Traefik** – Ingress controller: læser Ingress-ressourcer og fungerer som reverse proxy (port 80 → service → pods).

---

## Kubernetes-ressourcer vi bruger

| Ressource | Beskrivelse |
|-----------|-------------|
| **Namespace** | Virtuelt rum (fx `proxi`) til gruppering. |
| **Secret** | Følsomme data (fx DB-password); pods får dem som env. |
| **PVC** | Krav om disk; tildeles en volume (Postgres bruger den). |
| **Deployment** | Beskriver app: image, replicas, env. Opretter og holder pods kørende. |
| **Pod** | Mindste enhed: én eller flere containere. |
| **Service** | Fast netværksadresse (ClusterIP) til pods. Fx `proxi-db:5432`, `proxi-app:80`. |
| **Ingress** | Regler for indgående HTTP. Traefik sender / til proxi-app:80. |

---

## Docker & containere

- **Containere** – Isolerede processer med eget filsystem; deler kerne. Samme image kører overalt.
- **Docker** – I Proxi bruger vi Docker til at *bygge* image (Dockerfile → proxi-demo:latest). Image eksporteres til tar og importeres i K3s (containerd); selve kørsel sker i Kubernetes, ikke Docker.

---

## Diagrammer

Se forsiden på appen for Mermaid-diagrammer der viser:

1. **Fra kode til bruger** – Terraform → Proxmox → Ansible → K3s → Traefik → Bruger.
2. **K3s-cluster og pods** – CP med API + Traefik, workers med app- og postgres-pods, HTTP på port 80.
3. **Request-flow** – Browser → Traefik → Service → Pod (round-robin).
4. **K8s-ressourcer** – Namespace, Secret, PVC, Deployments, Services, Ingress og deres relation.

---

## Deploy og rollout

1. Redigér kode eller K8s YAML.
2. Kør fra Proxmox: `ansible-playbook -i inventory/hosts.ini playbooks/deploy-k8s.yml`
3. Playbooken bygger image, distribuerer, applicerer manifester og genstarter app-pods.

Se **Deploy-og-rollout.md** for detaljer.
