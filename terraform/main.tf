terraform {
  required_providers {
    libvirt = {
      source  = "dmacvicar/libvirt"
      version = "0.7.6"
    }
  }
}

provider "libvirt" {
  uri = "qemu:///system"
}

resource "libvirt_volume" "ubuntu_base" {
  name   = "ubuntu-base.qcow2"
  pool   = "default"
  source = "https://cloud-images.ubuntu.com/jammy/current/jammy-server-cloudimg-amd64.img"
  format = "qcow2"
}

resource "libvirt_volume" "ubuntu" {
  name           = "ubuntu.qcow2"
  pool           = "default"
  base_volume_id = libvirt_volume.ubuntu_base.id
  format         = "qcow2"
  size           = 21474836480
}

resource "libvirt_cloudinit_disk" "init" {
  name = "cloudinit.iso"
  pool = "default"

  user_data = <<-USERDATA
    #cloud-config
    users:
      - name: ubuntu
        sudo: ALL=(ALL) NOPASSWD:ALL
        shell: /bin/bash
        ssh_authorized_keys:
          - ${file("~/.ssh/id_rsa.pub")}
    package_update: true
  USERDATA

  network_config = <<-NETCONFIG
    version: 2
    ethernets:
      ens3:
        dhcp4: true
  NETCONFIG
}

resource "libvirt_domain" "vm" {
  cpu {
    mode = "host-passthrough"
  }

  name   = "devops-lab-vm"
  memory = 8192
  vcpu   = 6

  cloudinit = libvirt_cloudinit_disk.init.id

  disk {
    volume_id = libvirt_volume.ubuntu.id
  }

  network_interface {
    network_name   = "default"
    wait_for_lease = true
  }

  console {
    type        = "pty"
    target_port = "0"
    target_type = "serial"
  }
}

output "ip_address" {
  value = libvirt_domain.vm.network_interface[0].addresses[0]
}
