# Proxi demo-app

Node.js + Express med HTML/CSS/JS-frontend. Viser hvilken node (hostname + IP) du ramte – nyttigt bag load balancer.

## Lokal kørsel (uden Docker)

```bash
npm install
node server.js
```

Åbn http://localhost:3000

## Docker

```bash
docker compose up -d --build
```

Åbn http://localhost:3000

## Deploy med Ansible

Fra Ansible-mappen (kør fra Proxmox eller med ProxyJump):

```bash
ansible-playbook -i inventory/hosts.ini playbooks/deploy-app.yml
```

- Installerer Docker på alle tre noder og kører appen i container.
- Sætter nginx som load balancer på control plane (10.133.51.120) med round-robin til de to workers.
- Åbn http://10.133.51.120 – genindlæs for at se skifte mellem worker 1 og worker 2 (hostname + IP på siden).
