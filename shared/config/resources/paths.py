from dataclasses import dataclass
from pathlib import Path

from xdg_base_dirs import xdg_cache_home, xdg_data_home

HOME = str(Path.home())
XDG_DATA_HOME = str(xdg_data_home())
XDG_CACHE_HOME = str(xdg_cache_home())


@dataclass
class Directories:
    """Path constants for both the project and for the user level ansible installation at HOME/.ansible."""

    PROOT: str = XDG_DATA_HOME + "/dasbootstrap"
    SCROOT: str = PROOT + "/bin"
    LROOT: str = PROOT + "/lib"
    PBROOT: str = PROOT + "/ansible/playbooks"
    CROOT: str = PROOT + "/ansible"

    AHOME: str = HOME + "/.ansible"
    CHOME: str = AHOME + "/collections"
    RHOME: str = AHOME + "/roles"
    IHOME: str = AHOME + "/inventory"
    SVHOME: str = AHOME + "/global_vars"
    GVHOME: str = IHOME + "/group_vars"
    HVHOME: str = IHOME + "/host_vars"


@dataclass
class Requirements:
    COLLECTIONS_REQS: str = Directories.CHOME + "/requirements.yml"
    ROLES_REQS: str = Directories.RHOME + "/requirements.yml"


@dataclass
class Variables:
    ALL_SECURE_VARS: str = Directories.SVHOME + "/all.yaml"
    ALL_VARS: str = Directories.GVHOME + "/all.yaml"
    ALL_LXC_VARS: str = Directories.GVHOME + "/proxmox_all_lxc.yaml"


@dataclass
class Inventory:
    STATIC_HOSTS: str = Directories.IHOME + "/hosts.yaml"


@dataclass
class OperatingSystemFiles:
    KNOWN_HOSTS: str = str(Path.home()) + "/.ssh/known_hosts"
