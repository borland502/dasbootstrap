import ansible_runner
from dataclasses import dataclass
import yaml

from ansible.modules import *
from dasbootstrap_actions.resources import Paths,Resources

class Actions(object):

    def __init__(self, app_name="lxc"):
        self.app_name = app_name

    # ansible-inventory all --export --list --yaml -i "${INVENTORY_HOME}" --output "${A_HOSTS}" 2>&1 >/dev/null
    def dump_inventory(self):
        ansible_runner.run_command(executable_cmd="ansible-inventory",
                                          cmdline_args=['all', '--export', '--list', '--yaml', '-i',
                                                        str(Paths.IHOME), '--output', Resources.STATIC_HOSTS])

    # TODO: Add force option
    def update_collections(self):
        ansible_runner.run_command(executable_cmd="ansible-galaxy",
                                          cmdline_args=['collection', 'install', '-r', Resources.COLLECTIONS_REQS])

    # TODO: Add force option
    def update_roles(self):
        ansible_runner.run_command(executable_cmd="ansible-galaxy",
                                          cmdline_args=['role', 'install', '-r', Resources.ROLES_REQS])

    def create_lxc(self,app_name):
        ansible_runner.run_command(executable_cmd='ansible', cmdline_args=['localhost', '-m', 'import_role',
                                                                           '-a', "name=technohouser.proxmox.create_lxc",
                                                                           '-i', str(Paths.IHOME),
                                                                           '-e', '@' + str(Paths.HVHOME) + '/' + app_name + '.yaml',
                                                                           '-e', Resources.ALL_SECURE_VARS,
                                                                           '-e', Resources.ALL_VARS,
                                                                           '-e', Resources.ALL_LXC_VARS,
                                                                           '--user','root'])
    def destroy_lxc(self,app_name):
        ansible_runner.run_command(executable_cmd='ansible', cmdline_args=['localhost', '-m', 'import_role',
                                                                           '-a', "name=technohouser.destroy_lxc",
                                                                           '-i', str(Paths.IHOME),
                                                                           '-e', '@' + str(Paths.HVHOME) + '/' + app_name + '.yaml',
                                                                           '-e', Resources.ALL_SECURE_VARS,
                                                                           '-e', Resources.ALL_VARS,
                                                                           '-e', Resources.ALL_LXC_VARS,
                                                                           '--user','root'])
    def bootstrap_lxc(self, app_name):
        ansible_runner.run_command(executable_cmd='ansible', cmdline_args=[app_name, '-m', 'import_role',
                                                                                  '-a', "name=technohouser.bootstrap",
                                                                                  '-i', str(Paths.IHOME),
                                                                                  '-e', '@' + str(Paths.HVHOME) + '/' + app_name + '.yaml',
                                                                                  '-e', Resources.ALL_SECURE_VARS,
                                                                                  '-e', Resources.ALL_VARS,
                                                                                  '-e', Resources.ALL_LXC_VARS,
                                                                                  '--user','root'])

    # TODO cmdline_args dataclass
    def ansible_user_lxc(self, app_name):
        ansible_runner.run_command(executable_cmd='ansible', cmdline_args=[app_name, '-m', 'import_role',
                                                                                  '-a', "name=technohouser.ansible",
                                                                                  '-i', str(Paths.IHOME),
                                                                                  '-e', '@' + str(Paths.HVHOME) + '/' + app_name + '.yaml',
                                                                                  '-e', Resources.ALL_SECURE_VARS,
                                                                                  '-e', Resources.ALL_VARS,
                                                                                  '-e', Resources.ALL_LXC_VARS,
                                                                                  '--user','ansible'])

    def setup_lxc(self,app_name):
        self.create_lxc(app_name)
        self.dump_inventory()
        self.bootstrap_lxc(app_name)
        self.ansible_user_lxc(app_name)