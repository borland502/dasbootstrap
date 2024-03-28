from xdg_base_dirs import *
import ansible_runner
from pathlib import Path
from dataclasses import dataclass

@dataclass
class Paths:
    """Path constants for both the project and for the user level ansible installation at HOME/.ansilbe"""
    PROOT: Path = Path.joinpath(xdg_data_home(),"dasbootstrap")
    SCROOT: Path = Path.joinpath(PROOT, "bin")
    LROOT: Path = Path.joinpath(PROOT, "lib")

    AHOME: Path = Path.joinpath(Path.home(), ".ansible")
    CHOME: Path = Path.joinpath(AHOME, "collections")
    RHOME: Path = Path.joinpath(AHOME, "roles")
    IHOME: Path = Path.joinpath(AHOME, "inventory")
    GVHOME: Path = Path.joinpath(IHOME, "group_vars")
    HVHOME: Path = Path.joinpath(IHOME, "host_vars")
class Actions:

    def get_inventory():
        return ansible_runner.get_inventory(action="list", inventories=[f"{Paths.IHOME}"])