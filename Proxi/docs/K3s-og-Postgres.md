# K3s og Postgres – hvordan det hænger sammen

## Nuværende setup (Docker på VM’er)

- **Terraform** kloner VM’er (1 control plane, 2 workers) med statisk net (VLAN 551).
- **Ansible** installerer Docker på alle og deployer app-mappen til `/opt/proxi-app`.
- **Postgres** kører **kun på control plane**, via Docker Compose med profilen `controlplane`:
  - `docker compose --profile controlplane up -d --build` starter både `app` og `db`.
  - App på control plane får `NODE_DB_HOST=db` (Docker-netværkets service-navn).
- **Workers** kører kun app-containeren (`docker compose up -d --build`). De får `NODE_DB_HOST=<control-plane-ip>`, så de forbinder til Postgres på control plane over port 5432.
- **Nginx** på control plane fungerer som round-robin load balancer til workerne (port 3000). Brugeren rammer altid nginx på cp og bliver sendt videre til en af workerne.

Så: én fælles Postgres (på cp), flere app-instanser (cp + workers), load-balanced adgang via nginx.

---

## Hvis du senere kører med K3s

Med K3s vil du typisk:

1. **Node-appen** deploye som en **Deployment** med fx 2–3 replicas. K3s scheduler pods på noderne; du behøver ikke selv vælge hvilken VM der kører app.
2. **Postgres** køre som **StatefulSet** (eller Deployment) med en **PersistentVolumeClaim**, så data overlever pod-genstart. Du placere ofte Postgres-poden på én node (eller brug en dedikeret DB-node).
3. **Netværk:** App-pods får adgang til Postgres via en **Service** (fx `postgres.proxi.svc.cluster.local`). Du sætter i app’ens miljø `NODE_DB_HOST=postgres` (eller det Service-navn du vælger) og eksponerer ikke Postgres ud af klyngen, medmindre du vil.
4. **Ingress / LoadBalancer:** I stedet for nginx på control plane kan du bruge K3s’ indbyggede Traefik Ingress eller fx MetalLB som LoadBalancer og lade trafikken gå til app-Service, som round-robin til pod’erne.

Kort sagt: samme idé – én fælles database, flere app-instanser, load-balanced adgang – men med Kubernetes-ressourcer (Deployment, Service, Ingress, evt. StatefulSet + PVC) i stedet for Docker Compose og nginx på én VM.
