"""Paths Module."""

from __future__ import annotations

from pathlib import Path

from xdg_base_dirs import xdg_cache_home, xdg_config_home, xdg_data_home, xdg_state_home

# TODO: Replace all this with a KVStore

HOME = str(Path.home())
XDG_DATA_HOME = str(xdg_data_home())
XDG_CACHE_HOME = str(xdg_cache_home())
XDG_CONFIG_HOME = str(xdg_config_home())
XDG_STATE_HOME = str(xdg_state_home())


class Directories:
  """Path constants for both the project and for the user level ansible installation at HOME/.ansible."""

  PROOT: str = f"{XDG_DATA_HOME}/automation/dasbootstrap"
  PROJECT_ROOT: str = PROOT
  XDG_BIN_HOME: str = f"{HOME}/.local/bin"
  XDG_LIB_HOME: str = f"{PROOT}/.local/lib"
  PBROOT: str = f"{PROOT}/ansible/playbooks"
  PLAYBOOK_ROOT: str = PBROOT
  CROOT: str = f"{PROOT}/ansible"
  AHOME: str = f"{HOME}/.ansible"
  ANSIBLE_HOME: str = AHOME
  CHOME: str = f"{AHOME}/collections"
  RHOME: str = f"{AHOME}/roles"
  IHOME: str = f"{AHOME}/inventory"
  GVHOME: str = f"{IHOME}/group_vars"
  HVHOME: str = f"{IHOME}/host_vars"


class Requirements:
  """Ansible requirements yaml for collections and roles."""

  COLLECTIONS_REQS: str = f"{Directories.CHOME}/requirements.yml"
  ROLES_REQS: str = f"{Directories.RHOME}/requirements.yml"


class Variables:
  """Extra variables to pass to Ansible runners."""

  ALL_KVM_VARS: str = f"{Directories.GVHOME}/proxmox_all_kvm.yaml"
  ALL_VARS: str = f"{Directories.GVHOME}/all.yaml"
  ALL_LXC_VARS: str = f"{Directories.GVHOME}/proxmox_all_lxc.yaml"
  CHEZMOI_DATA: str = f"{Directories.GVHOME}/chezmoi_data.yaml"


class Inventory:
  """Source/Target for Inventory Actions."""

  STATIC_HOSTS: str = f"{Directories.IHOME}/hosts.yaml"
  STATIC_HOSTS_YAML: str = STATIC_HOSTS
  STATIC_HOSTS_TOML: str = f"{Directories.IHOME}/hosts.toml"
  DYNAMIC_NMAP: str = f"{Directories.IHOME}/nmap.yaml"
  DYNAMIC_PROXMOX: str = f"{Directories.IHOME}/proxmox.yaml"
  DYNAMIC_LDAP: str = f"{Directories.IHOME}/microsoft.ad.ldap.yaml"
  DYNAMIC_SQLITE: str = f"{Directories.IHOME}/sqlite.yaml"
  DBS_SQLITE: str = f"{XDG_STATE_HOME}/sqlite/dasbootstrap.db"
  INVENTORY_ALL: str = f"{Directories.IHOME}/inventory/"


class OperatingSystemFiles:
  """Operating System files used by Dasbootstrap."""

  KNOWN_HOSTS: str = str(Path.home()) + "/.ssh/known_hosts"
