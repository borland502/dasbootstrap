# Ansible Collection - `cielito.proxmox`

This collection groups several roles allowing to manage a [Proxmox VE](https://proxmox.com/en/proxmox-ve) cluster, providing an IaaS deployment.

First version includes the roles:

* [`cielito.proxmox.create_lxc`](roles/create_lxc), which previously was [`udelarinterior.proxmox_create_lxc`](https://galaxy.ansible.com/udelarinterior/proxmox_create_lxc), creates and starts an LXC container on a Proxmox VE system,

* [`cielito.proxmox.create_kvm`](roles/create_kvm), which previously was [`udelarinterior.proxmox_create_kvm`](https://galaxy.ansible.com/udelarinterior/proxmox_create_kvm), creates and starts a KVM virtual machine on a Proxmox VE system,

* [`cielito.proxmox.make_vm_template_unique`](roles/make_vm_template_unique), which previously was [`udelarinterior.make_vm_template_unique`](https://galaxy.ansible.com/udelarinterior/make_vm_template_unique), configures and makes accessible a KVM created with the previous role, chosing the option of clonning a Proxmox VE template,

* [`cielito.proxmox.firewall`](roles/firewall), which previously was [`udelarinterior.firewall_proxmox`](https://galaxy.ansible.com/udelarinterior/firewall_proxmox), configures Proxmox VE firewall of cluster and hosts.

* [`cielito.proxmox.users_and_groups`](roles/users_and_groups), which previously was [`udelarinterior.proxmox_users`](https://galaxy.ansible.com/udelarinterior/proxmox_users), configures Proxmox VE users, groups and persmissions of the cluster.

License
-------

(c) [Universidad de la República](https://www.udelar.edu.uy) (UdelaR), [Red de Unidades Informáticas de la UdelaR en el Interior](https://www.interior.edu.uy)

Licenced under GPL-3.0-or-later

See authors of each role.