terraform {
  required_providers {
    proxmox = {
      source  = "bpg/proxmox"
      version = "~> 0.68"
    }
  }
}

#################################
# VARIABLES
#################################

variable "pm_api_url" {
  type        = string
  description = "Proxmox API base URL (e.g. https://10.133.51.119:8006/ or https://host:8006/api2/json)"
}

variable "pm_api_token_id" {
  type        = string
  description = "Proxmox API Token ID (e.g. terraform@pve!terraform)"
}

variable "pm_api_token_secret" {
  type        = string
  description = "Proxmox API Token Secret"
  sensitive   = true
}

variable "target_node" {
  type        = string
  description = "Proxmox node name (e.g. pve)"
}

variable "clone_template_vmid" {
  type        = number
  description = "VMID of the template to clone from (e.g. ubuntu-template)"
  default     = 9000
}

# Netværk: statisk IP (ingen DHCP). Tilpas til jeres subnet/gateway.
variable "vm_network_gateway" {
  type        = string
  description = "Gateway for VM'erne (samme som Proxmox-host bruger)"
  default     = "10.133.51.1"
}

variable "vm_network_prefix" {
  type        = number
  description = "Netmask som prefix (fx 24 for /24)"
  default     = 24
}

variable "k3s_cp_ip" {
  type        = string
  description = "Statisk IP til k3s-cp-1 (uden /prefix)"
  default     = "10.133.51.120"
}

variable "k3s_worker_ips" {
  type        = list(string)
  description = "Statiske IP'er til k3s-worker-1 og k3s-worker-2 (uden /prefix)"
  default     = ["10.133.51.121", "10.133.51.122"]
}

# TRUNK + VLAN 551 (samme net som Proxmox 10.133.51.119). Hardcodet – ændr her hvis I skifter net.
variable "vm_network_vlan_id" {
  type        = number
  description = "VLAN tag på TRUNK (551 = 10.133.51.x sammen med Proxmox)"
  default     = 551
}

variable "vm_user_password" {
  type        = string
  description = "Password til brugeren ubuntu (Proxmox-konsol noVNC + SSH password-login). Sæt i tfvars – ikke commit."
  sensitive   = true
}

# Diskstørrelse i GB for root-disk på VM'erne (template-disk resizes til denne størrelse ved clone).
# K3s kræver plads – 32 GB anbefales. Template-disk skal være ≤ denne størrelse eller resizes.
variable "vm_disk_size_gb" {
  type        = number
  description = "Root-disk størrelse i GB (fx 32 for K3s). Template-disk resizes til denne ved clone."
  default     = 32
}

#################################
# PROVIDER (bpg/proxmox)
#################################

provider "proxmox" {
  endpoint  = replace(var.pm_api_url, "/api2/json/?$", "/")
  api_token = "${var.pm_api_token_id}=${var.pm_api_token_secret}"
  insecure  = true
}

#################################
# LOCALS (genbrugt VM-konfig)
#################################

locals {
  # Mathi's nøgle (fra fil når Terraform kører på Mathi's PC)
  ssh_public_key_mathi = trimspace(file("C:/Users/mathi/.ssh/id_ed25519.pub"))
  # Proxmox (root@pve) – SSH fra PVE til VM'erne uden password
  ssh_public_key_proxmox = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC9JtnYyine5bot1bvVmd8ZC8iSeHW7zqQKuilG2Cbc3se7E24gUeGzfHWncWpaa53y9lHz++h14GxBH0YOyjPSIgcgsOBoq2+4scbXq2q4wap80LdJn0QFFzU49xC3osy9XbO0nkHsIIUzmGcplEUzkPsKIwByF6P3dcBJrFYC31CFRJspLsneYxumeynGjZvmlhdjnOh0kccdD+FrqwxhDIYPQqirSENamqIMqrJXn4SwOaPrBpNWdNT2wuxPTsMc2DB+vLh5rr0YU3yAb04X1/kyRDxvOAuk/2AySn4oqiaXS1wn5eIwEcFVZpCNBazoZK3iOYc1r/D3+mydgbhOG1uY7A3O5bgSyGAwvTzBPj1QcrJ1tpUtQVrM3tUFU7J7W0XR+Sceehnx8taVoSlLVpFlAkwk1+UMBl3IoLKQZjC/pvrUnq99gKBOyg7knyD7QgdCFeEdOaFes4dR7qQ6VnCUPEiLA/fQklFwNgygZKb0ti2whKjOT4SE0RLkjdLzG1WkRASlO7c1sVgyotcmJBPXwhWRPNozPFHytz7AVCmmytE/SJpNsJvHPUqe4YTdgNBCQKTW69CLqhAHhaZNDchoYhnxsgnvE3LMY27O1WCL6pmQxJFJ+cA9ZIH4Ge1oVYxvUB1eF6vCc2bfb+n8rNVHlQsvkvHjmKB0W4GJOQ== root@pve"

  common_vm_config = {
    clone = {
      vm_id        = var.clone_template_vmid
      node_name    = var.target_node
      datastore_id = "Disks"
      full         = true
    }
    agent           = { enabled = false }
    stop_on_destroy = true
    cpu             = { cores = 2, type = "host" }
    memory          = { dedicated = 4096 }
    initialization = {
      datastore_id = "Disks"
      user_account = {
        username = "ubuntu"
        keys     = [local.ssh_public_key_mathi, local.ssh_public_key_proxmox]
      }
    }
    network_device   = { bridge = "TRUNK", model = "virtio", vlan_id = var.vm_network_vlan_id }
    operating_system = { type = "l26" }
  }

  # Statiske IP'er (til cloud-init og til outputs til Ansible)
  vm_cp_address    = "${var.k3s_cp_ip}/${var.vm_network_prefix}"
  vm_worker_addresses = [for ip in var.k3s_worker_ips : "${ip}/${var.vm_network_prefix}"]
}


#################################
# K3S CONTROL PLANE (1 node)
#################################

resource "proxmox_virtual_environment_vm" "k3s_control_plane" {
  name        = "k3s-cp-1"
  description = "K3s control plane"
  node_name   = var.target_node
  vm_id       = 100

  clone {
    vm_id        = local.common_vm_config.clone.vm_id
    node_name    = local.common_vm_config.clone.node_name
    datastore_id = local.common_vm_config.clone.datastore_id
    full         = local.common_vm_config.clone.full
  }

  agent {
    enabled = local.common_vm_config.agent.enabled
  }

  stop_on_destroy = local.common_vm_config.stop_on_destroy

  cpu {
    cores = local.common_vm_config.cpu.cores
    type  = local.common_vm_config.cpu.type
  }

  memory {
    dedicated = local.common_vm_config.memory.dedicated
  }

  disk {
    datastore_id = local.common_vm_config.clone.datastore_id
    interface    = "scsi0"
    size         = var.vm_disk_size_gb
  }

  initialization {
    datastore_id = local.common_vm_config.initialization.datastore_id
    ip_config {
      ipv4 {
        address = local.vm_cp_address
        gateway = var.vm_network_gateway
      }
    }
    user_account {
      username = local.common_vm_config.initialization.user_account.username
      keys     = local.common_vm_config.initialization.user_account.keys
      password = var.vm_user_password
    }
  }

  network_device {
    bridge  = local.common_vm_config.network_device.bridge
    model   = local.common_vm_config.network_device.model
    vlan_id = local.common_vm_config.network_device.vlan_id
  }

  operating_system {
    type = local.common_vm_config.operating_system.type
  }
}

#################################
# K3S WORKERS (2 nodes)
#################################

resource "proxmox_virtual_environment_vm" "k3s_worker" {
  count       = 2
  name        = "k3s-worker-${count.index + 1}"
  description = "K3s worker node ${count.index + 1}"
  node_name   = var.target_node
  vm_id       = 101 + count.index

  clone {
    vm_id        = local.common_vm_config.clone.vm_id
    node_name    = local.common_vm_config.clone.node_name
    datastore_id = local.common_vm_config.clone.datastore_id
    full         = local.common_vm_config.clone.full
  }

  agent {
    enabled = local.common_vm_config.agent.enabled
  }

  stop_on_destroy = local.common_vm_config.stop_on_destroy

  cpu {
    cores = local.common_vm_config.cpu.cores
    type  = local.common_vm_config.cpu.type
  }

  memory {
    dedicated = local.common_vm_config.memory.dedicated
  }

  disk {
    datastore_id = local.common_vm_config.clone.datastore_id
    interface    = "scsi0"
    size         = var.vm_disk_size_gb
  }

  initialization {
    datastore_id = local.common_vm_config.initialization.datastore_id
    ip_config {
      ipv4 {
        address = local.vm_worker_addresses[count.index]
        gateway = var.vm_network_gateway
      }
    }
    user_account {
      username = local.common_vm_config.initialization.user_account.username
      keys     = local.common_vm_config.initialization.user_account.keys
      password = var.vm_user_password
    }
  }

  network_device {
    bridge  = local.common_vm_config.network_device.bridge
    model   = local.common_vm_config.network_device.model
    vlan_id = local.common_vm_config.network_device.vlan_id
  }

  operating_system {
    type = local.common_vm_config.operating_system.type
  }
}

#################################
# OUTPUTS (til Ansible / inventar)
#################################

output "k3s_control_plane" {
  description = "K3s control plane VM (til Ansible)"
  value = {
    name  = proxmox_virtual_environment_vm.k3s_control_plane.name
    vm_id = proxmox_virtual_environment_vm.k3s_control_plane.vm_id
    node  = proxmox_virtual_environment_vm.k3s_control_plane.node_name
    ipv4  = try(proxmox_virtual_environment_vm.k3s_control_plane.ipv4_addresses[0], var.k3s_cp_ip)
  }
}

output "k3s_workers" {
  description = "K3s worker VMs (til Ansible)"
  value = [for i, w in proxmox_virtual_environment_vm.k3s_worker : {
    name  = w.name
    vm_id = w.vm_id
    node  = w.node_name
    ipv4  = try(w.ipv4_addresses[0], var.k3s_worker_ips[i])
  }]
}

output "k3s_ansible_inventory" {
  description = "Forslag til Ansible: brug disse hosts (IP kommer når agent er klar)"
  value = {
    control_plane = ["k3s-cp-1"]
    workers       = [for w in proxmox_virtual_environment_vm.k3s_worker : w.name]
  }
}
