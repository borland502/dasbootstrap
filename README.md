# Dasbootstrap

## Overview

Dasbootstrap is a loose wrapper around other efforts, including my own, to bootstrap containers, virtual machines, applications, and even dotfiles.  All personal automation is local in nature, but this project will be even more so -- centered on products I use and coherent enough to provide a leg up when the next personal project takes my fancy.  That is to say you'll best be served by the frameworks I wrap like Bootware, DebOps, Proxmox LXC roles, and Proxmox VE Helper-Scripts projects that do aim to provide extensibility and are written by automation experts.  I am still learning most of the products and languages that I employ so Dasbootstrap will likely be messy for some time.

Even cowboy-style DevOps needs some focal points at least, and those are:

1. Proxmox
2. Ansible
3. ZSH managed by Chezmoi

After playing around for a long time with other efforts Proxmox hits the sweet spot between professional grade and approachable as a hypervisor OS.  

TODO: A ton

## Example

```bash
./dbs setup test
./dbs destroy lxc test
```

## Links

[Bootware](https://github.com/scruffaluff/bootware)
[Buluma Roles](https://galaxy.ansible.com/ui/repo/published/buluma/roles/docs/)
[Linux Domain Management](https://github.com/EddyMaestroDev/linux_domain_mgmt)
[Proxmox VE Helper-Scripts](https://tteck.github.io/Proxmox/)
[Robert Debock Roles](https://robertdebock.nl/ansible.html)
[cielito.proxmox](https://galaxy.ansible.com/ui/repo/published/cielito/proxmox/content/role/create_lxc/)

## Sandbox 

arensb.truenas
debops.debops
linuxhq.linux
manala.roles
robertdebock.roles
buluma.roles
https://github.com/mullholland?tab=repositories
https://github.com/agaffney/ansible-synology-dsm/tree/master/tasks
https://github.com/BrynardSecurity-Ansible/ansible-role-domain-join/blob/main/tasks/main.yml
https://github.com/sgargel/linux_joindomain
https://github.com/schneidr/linux_joindomain
