# Dasbootstrap

## Install

### From Taskfile / Ansible Node Example

Install [Task](https://taskfile.dev/installation/)

```bash
* install:                      Install all pyprojects to local .venv
* lint:                         Runs linters
* test:                         Run unit tests
* update:                       Update dasbootstrap and ansible dependencies
* ansible:inventory:ldap:       Display inventory with the ansible ldap dynamic plugin
* ansible:inventory:nmap:       Display inventory with the ansible nmap dynamic plugin
* bin:system:update:            Update the local system
* create:kvm:                   Create a KVM by hostname
* create:lxc:                   Create an LXC by hostname
* destroy:lxc:                  Destroy an LXC by hostname

task create:lxc
```
### From pure shell

```bash
curl -L https://raw.githubusercontent.com/borland502/dasbootstrap/main/bin/dasbootstrap.sh \
  -o dasbootstrap.sh
  
chmod +x ./dasbootstrap.sh && ./dasbootstrap.sh  
```

In both cases [gum](https://github.com/charmbracelet/gum) is used to gather sensitive variables like the age 
encryption key and the key and token for the keepass database.

## Overview

Dasbootstrap is a loose wrapper around other efforts, including my own, to bootstrap containers, virtual machines, applications, and even dotfiles.  All personal automation is local in nature, but this project will be even more so -- centered on products I use and coherent enough to provide a leg up when the next personal project takes my fancy.  That is to say you'll best be served by the frameworks I wrap like cielito.proxmox, ansible-hombrew, and Proxmox VE Helper-Scripts projects that aim to provide extensibility and are written by automation experts.  I am still learning most of the products and languages that I employ here so Dasbootstrap will likely be messy for some time.

Even cowboy-style DevOps needs some focal points at least, and those are:

1. Proxmox
2. Terraform / Ansible / Taskfile
3. Python
4. ZSH managed by Chezmoi

## License

MIT unless attributed to another author

## Links

* [Taskfile.dev](https://taskfile.dev/installation/)
* [Buluma Roles](https://galaxy.ansible.com/ui/repo/published/buluma/roles/docs/)
* [Proxmox VE Helper-Scripts](https://tteck.github.io/Proxmox/)
* [Robert Debock Roles](https://robertdebock.nl/ansible.html)
* [cielito.proxmox](https://git.interior.edu.uy/cielito/proxmox)
* [ansible-homebrew](https://github.com/ProfessorManhattan/ansible-homebrew)
* [ansible-role-pyenv](https://github.com/staticdev/ansible-role-pyenv)
* [ansible-role-python-developer](https://github.com/staticdev/ansible-role-python-developer)
* [ansible-role-package](https://github.com/GROG/ansible-role-package)
* [install.doctor](https://github.com/megabyte-labs/install.doctor/tree/master)