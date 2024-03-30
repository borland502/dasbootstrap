from dataclasses import dataclass
from pathlib import Path
from dasbootstrap_actions.paths import Paths

@dataclass
class Resources(Paths):
    STATIC_HOSTS: str = str(Path.joinpath(Paths.IHOME, 'hosts.yaml'))
    COLLECTIONS_REQS: str = str(Path.joinpath(Paths.CHOME, "requirements.yml"))
    ROLES_REQS: str = str(Path.joinpath(Paths.RHOME, "requirements.yml"))
    DASBOOTSTRAP_DB: str = str(Path.joinpath(Paths.AHOME, "dasbootstrap.db"))
    ALL_SECURE_VARS: str = '@' + str(Path.joinpath(Paths.SVHOME, 'all.yaml'))
    ALL_VARS: str = '@' + str(Path.joinpath(Paths.GVHOME, 'all.yaml'))
    ALL_LXC_VARS: str = '@' + str(Path.joinpath(Paths.GVHOME, 'proxmox_all_lxc.yaml'))