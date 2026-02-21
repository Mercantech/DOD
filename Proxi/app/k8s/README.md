# K8s-manifester (Proxi app + Postgres)

Disse filer deployes til K3s via Ansible: `ansible-playbook playbooks/deploy-k8s.yml`.

| Fil | Beskrivelse |
|-----|-------------|
| `namespace.yaml` | Namespace `proxi` |
| `db-secret.yaml` | Hemmeligheder til Postgres og app (bruger/password/db) |
| `postgres.yaml` | PVC + Deployment + Service for Postgres 16 |
| `app.yaml` | Deployment (3 replicas) + Service for proxi-demo |
| `ingress.yaml` | Traefik Ingress – appen på http |

Efter deploy: Åbn http://\<control-plane-ip\> (fx http://10.133.51.120) og genindlæs for at se skifte mellem pods.

Manual apply (fra en maskine med kubeconfig):
```bash
kubectl apply -f namespace.yaml
kubectl apply -f db-secret.yaml
kubectl apply -f postgres.yaml
kubectl apply -f app.yaml
kubectl apply -f ingress.yaml
```
