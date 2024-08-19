# Dasbootstrap

## Install

### From Taskfile / Ansible Node Example

Install [Task](https://taskfile.dev/installation/)

```bash
task --list

# example output 
# * ans:create:kvm:                      Create a KVM by hostname
# * ans:create:lxc:                      Create an LXC by hostname
# * ans:destroy:lxc:                     Destroy an LXC by hostname
# * ans:dump-inventory:                  Dump the available ansible dynamic sources to a static hosts.yaml
# * ans:galaxy:collection:install:       Install collections
# * ans:galaxy:role:install:             Install roles
# * bin:system:update:                   Update the local system
# * chez:apply:                          Apply changes from downloaded dotfiles
# * chez:build:                          Build chezmoi and local dependencies
# * chez:lint:                           Lint templates, shell, and python code
# * chez:predeploy:                      Deploy chezmoi
# * inv:adhoc:inv:                       Use an ad-hoc ansible command to manually prime additional inventory variables
# * inv:inv:all:toml:                    Dump all available hosts in the Inventory to TOML
# * inv:inv:all:yaml:                    Dump all available hosts in the Inventory to YAML
# * inv:inv:nmap:toml:                   Use nmap to scan for all hosts with an open ssh port (22 or 2222) to TOML
# * inv:inv:proxmox:toml:                Use proxmox dynamic inventory module to dump all hosts to TOML
# * py:bandit:                           Run bandit
# * py:run_app:                          Run Automation Station
# * py:test:                             Run unit tests
```

```bash
# Example Commands
tg ans:create:lxc
task --global ans:create:lxc
```

### From pure shell

```bash
curl -L https://raw.githubusercontent.com/borland502/dasbootstrap/main/bin/dasbootstrap.sh \
  -o dasbootstrap.sh
  
chmod +x ./dasbootstrap.sh && ./dasbootstrap.sh  
```

## Overview

Dasbootstrap is a loose wrapper around other efforts, including my own, to bootstrap containers, virtual machines, applications, and even dotfiles.  All personal automation is local in nature, but this project will be even more so -- centered on products I use and coherent enough to provide a leg up when the next personal project takes my fancy.  That is to say you'll best be served by the frameworks I wrap like cielito.proxmox, ansible-hombrew, and Proxmox VE Helper-Scripts projects that aim to provide extensibility and are written by automation experts.  I am still learning most of the products and languages that I employ here so Dasbootstrap will likely be messy for some time.

Even cowboy-style DevOps needs some focal points at least, and those are:

1. Proxmox
2. Terraform / Ansible
3. Python / Poetry / Polylith / Taskfile
4. ZSH managed by Chezmoi

## License

MIT unless attributed to another author

## Links

* [Polylith](https://davidvujic.github.io/python-polylith-docs/)
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
