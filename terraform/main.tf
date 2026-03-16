// Terraform конфигурация для создания виртуальной машины через libvirt (KVM)
// Этот файл использует провайдер `dmacvicar/libvirt` и создаёт базовый образ,
// копию образа для VM, Cloud-Init диск и сам виртуальный домен.

terraform {
  required_providers {
    # Провайдер libvirt — взаимодействует с локальным QEMU/KVM (qemu:///system)
    libvirt = {
      source  = "dmacvicar/libvirt"
      version = "0.7.6"
    }
  }
}

// Настройки провайдера. `uri = "qemu:///system"` указывает на локальный
// демон libvirt (обычно доступен на хосте с KVM/virsh).
provider "libvirt" {
  uri = "qemu:///system"
}


// Создаём базовый том с образом Ubuntu Cloud (официальные cloud-images).
// Этот том служит как источник (base image) для копирования при создании VM.
resource "libvirt_volume" "ubuntu_base" {
  name   = "ubuntu-base.qcow2"
  pool   = "default"
  source = "https://cloud-images.ubuntu.com/jammy/current/jammy-server-cloudimg-amd64.img"
  format = "qcow2"
}


// Создаём рабочий том для конкретной VM на базе ubuntu_base. Параметр `size`
// задаёт размер диска в байтах (здесь 21474836480 = 20 GiB).
resource "libvirt_volume" "ubuntu" {
  name           = "ubuntu.qcow2"
  pool           = "default"
  base_volume_id = libvirt_volume.ubuntu_base.id
  format         = "qcow2"
  size           = 21474836480
}


// Cloud-init ISO диск — используется для первичной конфигурации гостевой ОС:
// создание пользователя, добавление SSH-ключа, обновление пакетов и настройка сети.
resource "libvirt_cloudinit_disk" "init" {
  name = "cloudinit.iso"
  pool = "default"

  # user_data — стандартный cloud-config для создания пользователя `ubuntu`
  # и установки ssh-ключа. Обратите внимание: путь ${file("~/.ssh/id_rsa.pub")}
  # читается локально на машине, где выполняется Terraform. Убедитесь, что
  # файл существует и содержит публичный ключ, который вы хотите добавить.
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

  # Простая сетeвая конфигурация: интерфейс ens3 получает IP по DHCP
  network_config = <<-NETCONFIG
    version: 2
    ethernets:
      ens3:
        dhcp4: true
  NETCONFIG
}


// Определение виртуальной машины (libvirt domain)
resource "libvirt_domain" "vm" {
  cpu {
    # host-passthrough позволяет гостю напрямую использовать инструкции CPU хоста
    mode = "host-passthrough"
  }

  name   = "devops-lab-vm"
  # Память в МБ (8192 = 8 GiB). Подберите значения под ваш хост
  memory = 8192
  # Количество виртуальных CPU
  vcpu   = 6

  # Подключаем cloud-init ISO чтобы автоматизировать первичную настройку гостя
  cloudinit = libvirt_cloudinit_disk.init.id

  disk {
    # Используем ранее созданный том ubuntu (копия базового образа)
    volume_id = libvirt_volume.ubuntu.id
  }

  network_interface {
    # Подключаем к дефолтной сети libvirt и ждём, пока гостю выдадут IP по DHCP
    network_name   = "default"
    wait_for_lease = true
  }

  console {
    # Включаем консоль (serial) для доступа к выводу гостя через virsh/virsh console
    type        = "pty"
    target_port = "0"
    target_type = "serial"
  }
}


// Выводим IP-адрес созданной VM после успешного apply. Значение берётся из
// первого сетевого интерфейса domain'а (network_interface[0].addresses[0]).
output "ip_address" {
  value = libvirt_domain.vm.network_interface[0].addresses[0]
}
