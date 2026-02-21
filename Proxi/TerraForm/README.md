# TerraForm – Proxmox K3s-cluster

Dette repo bruger TerraForm til at spinne et **K3s-cluster** på Proxmox: **1 control plane** + **2 workers**. Derefter kan Ansible installere K3s, joine workers og sætte ingress + MetalLB op. `terraform destroy` + `terraform apply` giver et rent cluster igen på få minutter.

---

## Hvad gør scriptet? (`main.tf`)

### 1. TerraForm-blok
- Kræver **Proxmox-provideren** [bpg/proxmox](https://registry.terraform.io/providers/bpg/proxmox/latest) (version ~> 0.68).

### 2. Variabler
- **`pm_api_url`**, **`pm_api_token_id`**, **`pm_api_token_secret`**, **`target_node`**, **`clone_template_vmid`** (default 9000) – som før.

### 3. Provider
- **bpg/proxmox** med endpoint, api_token og insecure.

### 4. VM-resources
- **Control plane:** `proxmox_virtual_environment_vm.k3s_control_plane` – navn **k3s-cp-1**, VMID **100**.
- **Workers:** `proxmox_virtual_environment_vm.k3s_worker` (count = 2) – **k3s-worker-1** (101), **k3s-worker-2** (102).
- Alle klones fra samme template til storage **Disks**, 2 cores, 4 GB RAM, **statisk IP** (ingen DHCP), bruger **ubuntu**, SSH-nøgle fra `C:/Users/mathi/.ssh/id_ed25519.pub`.

### 5. Netværk (statisk + TRUNK/VLAN)
- **`vm_network_gateway`** (default `10.133.51.1`) – gateway som VM'erne skal bruge (typisk gateway for det VLAN I bruger).
- **`vm_network_prefix`** (default `24`) – netmask som prefix.
- **`vm_network_vlan_id`** (default **551**) – **VLAN-tag på TRUNK**. Hardcodet til 551 (samme net som Proxmox 10.133.51.119). Ændr i `main.tf` hvis I skifter til andet VLAN.
- **`k3s_cp_ip`** (default `10.133.51.120`) – IP til k3s-cp-1.
- **`k3s_worker_ips`** (default `["10.133.51.121", "10.133.51.122"]`) – IP'er til worker 1 og 2.
- **`vm_user_password`** (obligatorisk, sensitiv) – password til brugeren **ubuntu**. Bruges til login i Proxmox-konsol (noVNC) og evt. SSH med password. Sæt i `terraform.tfvars` og tilføj filen til `.gitignore`.
- Tilpas gateway, VLAN og IP'er i `terraform.tfvars` så de matcher jeres net (og det VLAN I vælger). Sørg for at IP'erne ikke bruges af andre.

### 6. Outputs
- **`k3s_control_plane`** / **`k3s_workers`** – navn, vm_id, node, ipv4 (de konfigurerede statiske IP'er).
- **`k3s_ansible_inventory`** – hostnavne til Ansible. Brug output-ipv4 eller de samme værdier som i variablerne til `Ansible/inventory/hosts.ini`.

---

## Sådan laver du variabler i TerraForm

Variabler kan gives på tre måder (prioritet: 1 højest, 3 lavest):

### 1. `terraform.tfvars` (anbefalet til værdier)
Opret fx `terraform.tfvars` i mappen `TerraForm/`:

```hcl
pm_api_url             = "https://din-proxmox:8006/api2/json"
pm_api_token_id        = "terraform@pve!terraform"
pm_api_token_secret    = "dit-hemmelige-token"
target_node            = "pve"
clone_template_vmid   = 9000

# Netværk (statisk). Ved TRUNK + VLAN: sæt vm_network_vlan_id fx "552", og brug gateway/IP fra det VLAN (fx 10.0.552.x).
vm_network_gateway     = "10.133.51.1"
vm_network_prefix      = 24
# vm_network_vlan_id = 551   # default i main.tf (VLAN 551 = 10.133.51.x)
k3s_cp_ip              = "10.133.51.120"
k3s_worker_ips         = ["10.133.51.121", "10.133.51.122"]

# Password til ubuntu (Proxmox-konsol + SSH). Lad være med at committe tfvars!
vm_user_password      = "dit-adgangskode-til-ubuntu"
```

TerraForm læser automatisk `terraform.tfvars` og `*.auto.tfvars` ved plan/apply.

### 2. Miljøvariabler
```powershell
$env:TF_VAR_pm_api_url = "https://din-proxmox:8006/api2/json"
$env:TF_VAR_pm_api_token_id = "user@pam!terraform"
$env:TF_VAR_pm_api_token_secret = "dit-token"
$env:TF_VAR_target_node = "pve"
```

Prefix: **`TF_VAR_`** + variabelnavn (små bogstaver).

### 3. Kommandolinje med `-var`
```powershell
terraform plan -var="pm_api_url=https://din-proxmox:8006/api2/json" -var="target_node=pve"
```

**Vigtigt:** Sæt **aldrig** rigtige secrets i `main.tf`. Brug `terraform.tfvars` (og tilføj den til `.gitignore`) eller miljøvariabler.

---

## Sådan kører du TerraForm

**Forudsætning:** [TerraForm](https://www.terraform.io/downloads) er installeret, og du har oprettet variabler (fx via `terraform.tfvars` eller miljøvariabler).

```powershell
cd C:\Users\mathi\Documents\GitHub\Proxi\TerraForm
```

### Første gang (eller efter ændring af provider)
```powershell
terraform init
```
Henter provideren og forbereder backend.

### Se plan (hvad vil blive lavet/ændret)
```powershell
terraform plan
```

**Plan tager lang tid?** Terraform refresher state fra Proxmox; uden guest agent i VM’erne venter den op til 15 min per VM. Brug **uden refresh** (bruger sidst gemte state):
```powershell
terraform plan -refresh=false
```
Plan er så typisk færdig på sekunder. Brug derefter `terraform apply -refresh=false` for at udføre ændringerne uden at vente på agent. Efter VM’erne er opdateret til `agent.enabled = false` kan du køre normale `plan`/`apply` igen.

### Udfør ændringerne (opret/opdater VM)
```powershell
terraform apply
```
Skriv `yes` når TerraForm spørger. Ved langsom refresh: `terraform apply -refresh=false` (se ovenfor).

### Uden at blive spurgt om bekræftelse
```powershell
terraform apply -auto-approve
```

### Slet VM’en (destroy)
```powershell
terraform destroy
```

### Nyttige kommandoer
| Kommando              | Beskrivelse                    |
|-----------------------|--------------------------------|
| `terraform fmt`        | Formaterer `.tf`-filer         |
| `terraform validate`  | Tjekker syntaks                |
| `terraform show`       | Viser aktuelt state            |

---

## State mv (hvis du tidligere importerede som `k3s_server`)

Efter omskrivning til 1 control plane + 2 workers hedder control plane-ressourcen `k3s_control_plane`. Hvis du allerede har importeret VM 100 som `k3s_server`, flyt state så Terraform ikke vil destroy’e den:

```powershell
terraform state mv 'proxmox_virtual_environment_vm.k3s_server' 'proxmox_virtual_environment_vm.k3s_control_plane'
```

Derefter vil `terraform plan` kun vise de 2 nye workers + evt. en lille navneændring på CP (k3s-server-1 → k3s-cp-1).

## Importere en eksisterende VM

Hvis en VM findes i Proxmox men ikke i state:

```powershell
# Control plane (VMID 100)
terraform import proxmox_virtual_environment_vm.k3s_control_plane pve/100
# Worker 1 (VMID 101)
terraform import 'proxmox_virtual_environment_vm.k3s_worker[0]' pve/101
# Worker 2 (VMID 102)
terraform import 'proxmox_virtual_environment_vm.k3s_worker[1]' pve/102
```

---

## Fejlfinding: VM har IP men ingen kan ping

**Symptom:** VM’en viser fx 10.133.51.120 (via Proxmox eller `ip a` i konsol), men ping/SSH fra andre maskiner virker ikke.

**Årsag:** Med **TRUNK** og **vlan_id = 0** (ingen tag) er VM’en på den "rå" trunk – den er ikke i et konkret VLAN. Netværket forventer typisk trafik med et VLAN-tag (fx 552). Uden tag når trafikken ikke frem til 10.133.51.x-netværket.

**Løsning:** Sæt det VLAN I faktisk bruger for det net:
- I `terraform.tfvars`: `vm_network_vlan_id = 552` (eller det ID jeres 10.133.51.x / 10.0.552.x net bruger).
- Gateway og IP’er skal matche det VLAN (fx 10.0.552.1 og 10.0.552.x hvis det er VLAN552).
- Kør `terraform apply` (evt. destroy + apply så netværksændringen tages med).

---

## Opsummering

1. **Variabler** – defineret i `main.tf`, giv værdier via `terraform.tfvars`, `TF_VAR_*` eller `-var`.
2. **Kør:** `terraform init` → `terraform plan` → `terraform apply`.
3. Hold secrets ude af Git: brug `terraform.tfvars` i `.gitignore` eller miljøvariabler.
