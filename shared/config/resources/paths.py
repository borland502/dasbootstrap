"""Paths Module."""

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
  XDG_DATA_BIN: str = PROOT + "/bin"
  XDG_DATA_HOME: str = PROOT + "/lib"
  PBROOT: str = PROOT + "/ansible/playbooks"
  CROOT: str = PROOT + "/ansible"

  AHOME: str = HOME + "/.ansible"
  CHOME: str = AHOME + "/collections"
  RHOME: str = AHOME + "/roles"
  IHOME: str = AHOME + "/inventory"
  GVHOME: str = IHOME + "/group_vars"
  HVHOME: str = IHOME + "/host_vars"


@dataclass
class Requirements:
  """Ansible requirements yaml for collections and roles."""

  COLLECTIONS_REQS: str = Directories.CHOME + "/requirements.yml"
  ROLES_REQS: str = Directories.RHOME + "/requirements.yml"


@dataclass
class Variables:
  """Extra variables to pass to Ansible runners."""

  ALL_VARS: str = Directories.GVHOME + "/all.yaml"
  ALL_LXC_VARS: str = Directories.GVHOME + "/proxmox_all_lxc.yaml"


@dataclass
class Inventory:
  """Source/Target for Inventory Actions."""

  STATIC_HOSTS: str = Directories.IHOME + "/hosts.yaml"
  DBS_SQLITE: str = Directories.AHOME + "/dasbootstrap.db"


@dataclass
class OperatingSystemFiles:
  """Operating System files used by Dasbootstrap."""

  KNOWN_HOSTS: str = str(Path.home()) + "/.ssh/known_hosts"
