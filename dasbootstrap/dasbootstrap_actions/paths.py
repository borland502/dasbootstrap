from dataclasses import dataclass
from pathlib import Path
from xdg_base_dirs import *

@dataclass
class Paths:
    """Path constants for both the project and for the user level ansible installation at HOME/.ansilbe"""
    PROOT: Path = Path.joinpath(xdg_data_home(),"dasbootstrap")
    SCROOT: Path = Path.joinpath(PROOT, "bin")
    LROOT: Path = Path.joinpath(PROOT, "lib")
    CROOT: Path = Path.joinpath(xdg_cache_home(), "ansible")

    AHOME: Path = Path.joinpath(Path.home(), ".ansible")
    CHOME: Path = Path.joinpath(AHOME, "collections")
    RHOME: Path = Path.joinpath(AHOME, "roles")
    IHOME: Path = Path.joinpath(AHOME, "inventory")
    SVHOME: Path = Path.joinpath(AHOME, "global_vars")
    GVHOME: Path = Path.joinpath(IHOME, "group_vars")
    HVHOME: Path = Path.joinpath(IHOME, "host_vars")