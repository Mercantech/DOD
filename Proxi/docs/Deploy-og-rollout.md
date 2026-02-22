# Deploy og rollout – hvordan vi ruller ændringer ud

## Kort flow

1. **Ændringer** – Redigér app-kode (`app/`), K8s-manifester (`app/k8s/`) eller Ansible-playbooks.
2. **Kør fra Proxmox** – `ansible-playbook -i inventory/hosts.ini playbooks/deploy-k8s.yml`
3. **Resultat** – Nyt image bygges, distribueres til alle noder, manifester appliceres, app-pods genstartes (rolling update).

---

## Hvad sker der når du kører deploy-k8s.yml?

| Trin | Beskrivelse |
|------|-------------|
| **Play 1** (control plane) | Syncer `app/` til VM, bygger Docker-image `proxi-demo:latest`, eksporterer til tar, fetcher tar til PVE. |
| **Play 2** (alle noder) | Kopierer image-tar fra PVE til hver node, importerer i K3s containerd (`k3s ctr images import`). |
| **Play 3** (control plane) | Kopierer `app/k8s/` til VM, `kubectl apply` (namespace først, derefter resten), venter på Postgres + app rollout, **rollout restart** af proxi-app (så pods henter ny image), viser status. |

Efter kørsel har alle tre noder det nyeste image, og app-pods er genstartet så de bruger det.

---

## Kun app-kode ændret (fx frontend eller server.js)

- Redigér filer i `app/` (fx `public/index.html`, `server.js`).
- Kør:  
  `ansible-playbook -i inventory/hosts.ini playbooks/deploy-k8s.yml`  
- Playbooken bygger et nyt image, pusher det til noderne og genstarter deployment – du behøver ikke ændre noget i K8s YAML.

---

## Kun K8s-manifester ændret (fx replicas, env, ingress)

- Redigér filer i `app/k8s/`.
- Kør samme playbook – build/import kan køre (idempotent), og `kubectl apply -f` opdaterer ressourcer. App-pods genstartes også (kan undværes her; du kan kommentere rollout-restart-tasken ud hvis du vil spare tid).

---

## Kun Ansible-playbooks ændret

- Kør den relevante playbook (fx `k3s.yml` eller `deploy-k8s.yml`) – ingen ændringer i app eller k8s behøves.

---

## Hurtig genstart af app-pods (uden at bygge nyt image)

Hvis du bare vil genstarte app-pods (fx efter manuel ændring af Secret eller for at rydde hukommelse):

```bash
ssh ubuntu@10.133.51.120 'sudo kubectl --kubeconfig=/etc/rancher/k3s/k3s.yaml rollout restart deployment/proxi-app -n proxi'
```

---

## Adgang til appen

- **Fra Proxmox / samme net:** http://10.133.51.120  
- **Fra bærbar (kun SSH til Proxmox):**  
  `ssh -L 8080:10.133.51.120:80 root@<proxmox-ip>`  
  Derefter: http://localhost:8080
