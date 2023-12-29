# Dasbootstrap

## Overview

Dasbootstrap is a loose wrapper around other efforts, including my own, to bootstrap containers, virtual machines, applications, and even dotfiles.  All personal automation is local in nature, but this project will be even more so -- centered on products I use and coherent enough to provide a leg up when the next personal project takes my fancy.  That is to say you'll best be served by the frameworks I wrap like Bootware, DebOps, and Proxmox VE Helper-Scripts projects that do aim to provide extensibility and are written by automation experts.  I am still learning most of the products and languages that I employ so Dasbootstrap will likely be messy for some time.

Even cowboy-style DevOps needs some focal points at least, and those are:

1. Proxmox
2. Ansible
3. ZSH managed by Chezmoi

After playing around for a long time with other efforts Proxmox hits the sweet spot between professional grade and approachable as a hypervisor OS.

## TODO

1. Automatic Domain Sign On
2. Modify proxmox lxc containers to allow unpriviledged domain users
3. Fix or remove molecule tests

## Links

[Bootware](https://github.com/scruffaluff/bootware)
[Buluma Roles](https://galaxy.ansible.com/ui/repo/published/buluma/roles/docs/)
[Linux Domain Management](https://github.com/EddyMaestroDev/linux_domain_mgmt)
[Proxmox VE Helper-Scripts](https://tteck.github.io/Proxmox/)
[UdelaRInterior/ansible-role-proxmox-create-lxc](https://github.com/UdelaRInterior/ansible-role-proxmox-create-lxc)