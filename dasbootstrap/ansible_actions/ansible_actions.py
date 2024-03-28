from xdg_base_dirs import *
import ansible_runner
from pathlib import Path
from dataclasses import dataclass
import yaml

from ansible.modules import *

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
    GVHOME: Path = Path.joinpath(IHOME, "group_vars")
    HVHOME: Path = Path.joinpath(IHOME, "host_vars")

@dataclass
class Resources(Paths):
    STATIC_HOSTS: str = str(Path.joinpath(Paths.IHOME, 'hosts.yaml'))
    COLLECTIONS_REQS: str = str(Path.joinpath(Paths.CHOME, "requirements.yml"))
    ROLES_REQS: str = str(Path.joinpath(Paths.RHOME, "requirements.yml"))
    ALL_VARS: str = '@' + str(Path.joinpath(Paths.GVHOME, 'all.yaml'))
    ALL_LXC_VARS: str = '@' + str(Path.joinpath(Paths.GVHOME, 'proxmox_all_lxc.yaml'))

class Actions:

    # ansible-inventory all --export --list --yaml -i "${INVENTORY_HOME}" --output "${A_HOSTS}" 2>&1 >/dev/null
    def dump_inventory(self):
        return ansible_runner.run_command(executable_cmd="ansible-inventory",
                                          cmdline_args=['all', '--export', '--list', '--yaml', '-i',
                                                        str(Paths.IHOME), '--output', Resources.STATIC_HOSTS])

    # TODO: Add force option
    def update_collections(self):
        return ansible_runner.run_command(executable_cmd="ansible-galaxy",
                                          cmdline_args=['collection', 'install', '-r', Resources.COLLECTIONS_REQS])

    # TODO: Add force option
    def update_roles(self):
        return ansible_runner.run_command(executable_cmd="ansible-galaxy",
                                          cmdline_args=['roles', 'install', '-r', Resources.ROLES_REQS])

    def create_lxc(self,app_name):
        return ansible_runner.run_command(executable_cmd='ansible', cmdline_args=['localhost', '-m', 'import_role',
                                                                           '-a', "name=technohouser.proxmox.create_lxc",
                                                                           '-i', str(Paths.IHOME),
                                                                           '-e', '@' + str(Paths.HVHOME) + '/' + app_name + '.yaml',
                                                                           '-e', Resources.ALL_VARS,
                                                                           '-e', Resources.ALL_LXC_VARS,
                                                                           '--user','root'])
    def destroy_lxc(self, app_name):
        return ansible_runner.run_command(executable_cmd='ansible', cmdline_args=['localhost', '-m', 'import_role',
                                                                           '-a', "name=technohouser.destroy_lxc",
                                                                           '-i', str(Paths.IHOME),
                                                                           '-e', '@' + str(Paths.HVHOME) + '/' + app_name + '.yaml',
                                                                           '-e', Resources.ALL_VARS,
                                                                           '-e', Resources.ALL_LXC_VARS,
                                                                           '--user','root'])
    def bootstrap_lxc(self, app_name):
        return ansible_runner.run_command(executable_cmd='ansible', cmdline_args=['localhost', '-m', 'import_role',
                                                                                  '-a', "name=technohouser.bootstrap",
                                                                                  '-i', str(Paths.IHOME),
                                                                                  '-e', '@' + str(Paths.HVHOME) + '/' + app_name + '.yaml',
                                                                                  '-e', Resources.ALL_VARS,
                                                                                  '-e', Resources.ALL_LXC_VARS,
                                                                                  '--user','root'])

    # TODO cmdline_args dataclass
    def ansible_user_lxc(self, app_name):
        return ansible_runner.run_command(executable_cmd='ansible', cmdline_args=['localhost', '-m', 'import_role',
                                                                                  '-a', "name=technohouser.ansible",
                                                                                  '-i', str(Paths.IHOME),
                                                                                  '-e', '@' + str(Paths.HVHOME) + '/' + app_name + '.yaml',
                                                                                  '-e', Resources.ALL_VARS,
                                                                                  '-e', Resources.ALL_LXC_VARS,
                                                                                  '--user','ansible'])