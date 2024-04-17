# Dasbootstrap

## Overview

Dasbootstrap is a loose wrapper around other efforts, including my own, to bootstrap containers, virtual machines, applications, and even dotfiles.  All personal automation is local in nature, but this project will be even more so -- centered on products I use and coherent enough to provide a leg up when the next personal project takes my fancy.  That is to say you'll best be served by the frameworks I wrap like Bootware, DebOps, Proxmox LXC roles, and Proxmox VE Helper-Scripts projects that do aim to provide extensibility and are written by automation experts.  I am still learning most of the products and languages that I employ so Dasbootstrap will likely be messy for some time.

Even cowboy-style DevOps needs some focal points at least, and those are:

1. Proxmox
2. Ansible
3. ZSH managed by Chezmoi

After playing around for a long time with other efforts Proxmox hits the sweet spot between professional grade and approachable as a hypervisor OS.  

## Languages

The language used is primarily python and executed via ansible runners.  [Typer](https://github.com/tiangolo/typer) provides a quick and easy cli wrapper.

## Design

This project houses mostly templates with only the playbooks and roles executed locally.  Inventory, Collections, Roles, Vars, etc are in ~/.ansible.  Each host var file has enough info in it to create the lxc/qemu container as well as the intended app to install afterwards.

This project also checks out my dotfiles project and sets up that config with chezmoi

# TODO: Lots

## Example

```bash
./dbs create --app-name "sample-lxc"
./dbs destroy --app-name "sample-lxc"
```

```text
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                         │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.  │
│ --help                        Show this message and exit.                                                       │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ create               Creates and sets up a new LXC container, installing favorites, and creating a service user │
│ destroy              Destroys an existing LXC container.                                                        │
│ dump-inventory       Dump the inventory to hosts.yaml                                                           │
│ update-collections   Updates Ansible collections from requirements.                                             │
│ update-facts         Updates facts for all managed hosts.                                                       │
│ update-roles         Updates Ansible roles from requirements.                                                   │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Development Commands

```
poe 
```

## Links

* [Bootware](https://github.com/scruffaluff/bootware)
* [Buluma Roles](https://galaxy.ansible.com/ui/repo/published/buluma/roles/docs/)
* [Linux Domain Management](https://github.com/EddyMaestroDev/linux_domain_mgmt)
* [Proxmox VE Helper-Scripts](https://tteck.github.io/Proxmox/)
* [Robert Debock Roles](https://robertdebock.nl/ansible.html)
* [cielito.proxmox](https://galaxy.ansible.com/ui/repo/published/cielito/proxmox/content/role/create_lxc/)
