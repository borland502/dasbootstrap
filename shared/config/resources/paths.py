"""Paths Module."""

from dataclasses import dataclass
from pathlib import Path

from xdg_base_dirs import (
    xdg_cache_home,
    xdg_data_home,
    xdg_config_home,
    xdg_state_home,
)

# TODO: Replace all this with a KVStore

HOME = str(Path.home())
XDG_DATA_HOME = str(xdg_data_home())
XDG_CACHE_HOME = str(xdg_cache_home())
XDG_CONFIG_HOME = str(xdg_config_home())
XDG_STATE_HOME = str(xdg_state_home())


class Directories:
    """Path constants for both the project and for the user level ansible installation at HOME/.ansible."""

    PROOT: str = XDG_DATA_HOME + "/automation/dasbootstrap"
    PROJECT_ROOT: str = PROOT
    XDG_BIN_HOME: str = HOME + "/.local" + "/bin"
    XDG_LIB_HOME: str = PROOT + "/.local" + "/lib"
    PBROOT: str = PROOT + "/ansible/playbooks"
    PLAYBOOK_ROOT: str = PBROOT
    CROOT: str = PROOT + "/ansible"
    AHOME: str = HOME + "/.ansible"
    ANSIBLE_HOME: str = AHOME
    CHOME: str = AHOME + "/collections"
    RHOME: str = AHOME + "/roles"
    IHOME: str = AHOME + "/inventory"
    GVHOME: str = IHOME + "/group_vars"
    HVHOME: str = IHOME + "/host_vars"


class Requirements:
    """Ansible requirements yaml for collections and roles."""

    COLLECTIONS_REQS: str = Directories.CHOME + "/requirements.yml"
    ROLES_REQS: str = Directories.RHOME + "/requirements.yml"


class Variables:
    """Extra variables to pass to Ansible runners."""

    ALL_KVM_VARS: str = Directories.GVHOME + "/proxmox_all_kvm.yaml"
    ALL_VARS: str = Directories.GVHOME + "/all.yaml"
    ALL_LXC_VARS: str = Directories.GVHOME + "/proxmox_all_lxc.yaml"


class Inventory:
    """Source/Target for Inventory Actions."""

    STATIC_HOSTS: str = Directories.IHOME + "/hosts.yaml"
    DBS_SQLITE: str = XDG_STATE_HOME + "/sqlite/dasbootstrap.db"


class OperatingSystemFiles:
    """Operating System files used by Dasbootstrap."""

    KNOWN_HOSTS: str = str(Path.home()) + "/.ssh/known_hosts"
