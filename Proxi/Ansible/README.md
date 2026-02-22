# Ansible (Proxi K3s)

Kør playbooks mod K3s-clusteret (VM'er skabt med Terraform).

## Test forbindelse (ping)

Når VM'erne er startet (efter Terraform apply), vent evt. 10–20 sekunder til cloud-init har sat IP, og kør ping fra et sted der **kan nå 10.133.51.120–122** (se nedenfor).

Vellykket output: `pong` fra alle tre hosts (k3s-cp-1, k3s-worker-1, k3s-worker-2).

### Din PC kan nå Proxmox (10.133.51.119) men ikke VM'erne (.120–.122)

VM'erne er i **VLAN 551**; din PC er typisk på et andet net, så SSH fra PC til VM'erne når ikke frem. **Kør Ansible fra Proxmox** i stedet – Proxmox er i samme net som VM'erne.

**Fra Proxmox (pve):**
```bash
# SSH ind på Proxmox fra din PC:  ssh root@10.133.51.119

# På pve: klon repo (eller kopiér Ansible-mappen), og sæt din SSH-nøgle til ubuntu
apt update && apt install -y ansible git
git clone https://github.com/mercantech/Proxi.git   # eller scp Ansible-mappen over
cd Proxi/Ansible

# Kopiér din private nøgle til pve (så Ansible kan SSH til VM'erne som ubuntu).
# Fra din PC:  scp ~/.ssh/id_ed25519 root@10.133.51.119:/root/.ssh/
# På pve:  chmod 600 /root/.ssh/id_ed25519

# På pve – ret inventory så nøgle står under /root/.ssh:
sed -i 's|~/.ssh/id_ed25519|/root/.ssh/id_ed25519|' inventory/hosts.ini

ansible k3s_cluster -m ping -i inventory/hosts.ini
```

**Alternativ: kør Ansible fra din PC via ProxyJump (SSH gennem Proxmox)**  
Så behøver du ikke installere Ansible på pve – trafikken går PC → Proxmox → VM. Opret en ekstra inventory-fil eller tilføj til `[k3s_cluster:vars]`:

```ini
ansible_ssh_common_args='-o ProxyCommand="ssh -W %h:%p -q root@10.133.51.119"'
```

(Kræver at din PC kan SSH til root@10.133.51.119, og at Proxmox kan SSH til ubuntu@10.133.51.120/121/122 – dvs. din offentlige nøgle skal ligge både på pve og i VM'ernes ubuntu authorized_keys.)

## Playbooks

| Playbook | Beskrivelse |
|----------|-------------|
| `playbooks/k3s.yml` | Installerer K3s (server på control plane, agent på workers). Kør først. |
| `playbooks/deploy-k8s.yml` | **K3s-native:** Bygger app-image, loader i K3s, deployer Postgres + app som Deployments/Ingress. |
| `playbooks/deploy-app.yml` | Docker-baseret: Node-app + docker-compose på alle noder + nginx load balancer. |

### K3s-flow (anbefalet)

Fra Proxmox (eller med ProxyJump):

```bash
cd Proxi/Ansible
ansible k3s_cluster -m ping -i inventory/hosts.ini
ansible-playbook -i inventory/hosts.ini playbooks/k3s.yml
ansible-playbook -i inventory/hosts.ini playbooks/deploy-k8s.yml
```

Åbn http://10.133.51.120 – Traefik Ingress sender trafikken til app-pods på alle noder.

### Docker-flow (alternativ)

`ansible-playbook -i inventory/hosts.ini playbooks/deploy-app.yml` – Åbn http://10.133.51.120 og genindlæs for at se skifte mellem worker 1 og 2.

## Inventory

- `inventory/hosts.ini` – statiske IP'er for k3s-cp-1, k3s-worker-1, k3s-worker-2.
- Skal matche de IP'er I sætter i Terraform (`k3s_cp_ip`, `k3s_worker_ips` i `terraform.tfvars`). Hvis I ændrer netværk der, opdater også `hosts.ini`.
- SSH: bruger `ubuntu`, nøgle `~/.ssh/id_ed25519`.

## Kør Ansible

**Windows (Ansible understøtter ikke Windows som control node):** brug WSL eller Docker.

### WSL (Ubuntu)

```bash
cd /mnt/c/Users/mathi/Documents/GitHub/Proxi/Ansible
sudo apt update && sudo apt install -y ansible
ansible k3s_cluster -m ping
ansible-playbook playbooks/k3s.yml
```

### Alpine / dev container (Docker Desktop-shell, etc.)

Alpine har ikke `ansible` i apk og tillader ikke `pip install` i system-Python. Brug et venv:

```bash
cd /mnt/host/c/Users/mathi/Documents/GitHub/Proxi/Ansible

# Python, pip og SSH-klient (Ansible bruger ssh til at forbinde til VM'erne)
apk add --no-cache python3 py3-pip openssh-client

# Virtuelt miljø + Ansible
python3 -m venv .venv
. .venv/bin/activate
# Alpine kan stadig give "externally-managed-environment" i venv – brug da:
pip install ansible --break-system-packages

# SSH-nøgle (når du kører fra Docker-host-mount)
export ANSIBLE_SSH_PRIVATE_KEY_FILE="/mnt/host/c/Users/mathi/.ssh/id_ed25519"

# Test (brug -i fordi world-writable mappe får Ansible til at ignorere ansible.cfg)
ansible k3s_cluster -m ping -i inventory/hosts.ini
ansible-playbook playbooks/k3s.yml -i inventory/hosts.ini
```

Næste gang du åbner et nyt shell: `. .venv/bin/activate`, evt. `export ANSIBLE_SSH_PRIVATE_KEY_FILE=...`, og brug altid `-i inventory/hosts.ini` når mappen er et Windows-mount (world-writable).

### Docker (uden install i WSL)

Fra PowerShell i `Ansible`-mappen:

```powershell
docker run --rm -it -v "${PWD}:/work" -w /work -v "${HOME}/.ssh:/root/.ssh:ro" cytopia/ansible ansible k3s_cluster -m ping
```

### Playbooks (reference)

- `playbooks/k3s.yml` – K3s server på control plane, agent på workers (Traefik følger med).
- `playbooks/deploy-k8s.yml` – App + Postgres som Kubernetes-ressourcer; se også `../app/k8s/README.md`.
