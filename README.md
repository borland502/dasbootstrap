# Dasbootstrap

## Overview

Dasbootstrap is a loose wrapper around other efforts, including my own, to bootstrap containers, virtual machines, applications, and even dotfiles.  All personal automation is local in nature, but this project will be even more so -- centered on products I use and coherent enough to provide a leg up when the next personal project takes my fancy.  That is to say you'll best be served by the frameworks I wrap like cielito.proxmox, ansible-hombrew, and Proxmox VE Helper-Scripts projects that aim to provide extensibility and are written by automation experts.  I am still learning most of the products and languages that I employ here so Dasbootstrap will likely be messy for some time.

Even cowboy-style DevOps needs some focal points at least, and those are:

1. Proxmox
2. Ansible / Python
3. ZSH managed by Chezmoi

## Languages

The language used is primarily python and executed via ansible runners.  [Typer](https://github.com/tiangolo/typer) provides a quick and easy cli wrapper.

## Design

This project houses mostly templates with only the playbooks, collections, and roles executed locally.  Sensitive Inventory, Vars, etc are in ~/.ansible.  Each host var file has enough info in it to create the lxc/qemu container as well as the intended app to install afterwards.

This project also checks out my dotfiles project and sets up that config with chezmoi

# TODO: Lots

## Example

```bash
task --list
task dbs:run -- dump-inventory
task dbs:run -- create --app-name 'lxc'
task dbs:run -- destroy --app-name 'lxc'
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
task: Available tasks for this project:
* build:all:               Build all pyprojects and the shared libraries for them
* dbs:run:                 General alias for `poetry run python -m dasbootstrap` <command>
* install:all:local:       Install all pyprojects to local .venv
* tests:functional:        Runs all actions against a live proxmox server
* tests:integration:       Runs molecule integration and pytest unit/integration tests
* tools:bandit:            Run bandit
* tools:ruff:check:        Run ruff
* tools:ruff:format:       Format code
```

## License

MIT unless attributed to another author

## Links

* [Buluma Roles](https://galaxy.ansible.com/ui/repo/published/buluma/roles/docs/)
* [Proxmox VE Helper-Scripts](https://tteck.github.io/Proxmox/)
* [Robert Debock Roles](https://robertdebock.nl/ansible.html)
* [cielito.proxmox](https://git.interior.edu.uy/cielito/proxmox)
* [ansible-homebrew](https://github.com/ProfessorManhattan/ansible-homebrew)
* [ansible-role-pyenv](https://github.com/staticdev/ansible-role-pyenv)
* [ansible-role-python-developer](https://github.com/staticdev/ansible-role-python-developer)
* [ansible-role-package](https://github.com/GROG/ansible-role-package)
* [install.doctor](https://github.com/megabyte-labs/install.doctor/tree/master)