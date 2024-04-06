import ansible_runner
from dataclasses import dataclass
import yaml

from ansible.modules import *
from dasbootstrap_actions.resources import Paths,Resources
from dasbootstrap.utils import *

INVENTORY: [] = ['-i', str(Paths.IHOME)]
VARS: [] = INVENTORY + ['-e', Resources.ALL_SECURE_VARS,
        '-e', Resources.ALL_VARS,
        '-e', Resources.ALL_LXC_VARS]


class Actions(object):

    def __init__(self, app_name="lxc"):
        self.app_name = app_name
        self.app_path = f"@{Paths.HVHOME}/{app_name}.yaml"

    # TODO: Builder pattern for cmdline_args
    def dump_inventory(self):
        ansible_runner.run_command(executable_cmd="ansible-inventory",
                                          cmdline_args=['all', '--export', '--list', '--yaml'] + INVENTORY +
                                                        ['--output', Resources.STATIC_HOSTS])

    def update_collections(self):
        ansible_runner.run_command(executable_cmd="ansible-galaxy",
                                          cmdline_args=['collection', 'install', '-r', Resources.COLLECTIONS_REQS,
                                                        '--force'])

    def update_facts(self):
        ansible_runner.run_command(executable_cmd="ansible",
                                   cmdline_args=['all', '-m', 'setup'] + VARS +  ['--user',
                                    'ansible'])

    def update_roles(self):
        ansible_runner.run_command(executable_cmd="ansible-galaxy",
                                          cmdline_args=['role', 'install', '-r', Resources.ROLES_REQS, '--force'])

    def create_lxc(self,app_name):
        ansible_runner.run_command(executable_cmd='ansible',
                                   cmdline_args=['localhost', '-m', 'import_role',
                                                '-a', "name=technohouser.proxmox.create_lxc", '-e', self.app_path]
                                                + VARS + ['--user','root'])

    def destroy_lxc(self,app_name):
        ansible_runner.run_command(executable_cmd='ansible',
                                   cmdline_args=['localhost', '-m', 'import_role',
                                   '-a', "name=technohouser.destroy_lxc", '-e', self.app_path]
                                                + VARS + ['--user','root'])

    def bootstrap_lxc(self, app_name):
        ansible_runner.run_command(executable_cmd='ansible', cmdline_args=[app_name, '-m', 'import_role',
                                                                                  '-a', "name=technohouser.bootstrap"]
                                                                                  + VARS +
                                                                                  ['-e', self.app_path,'--user','root'])

    def ansible_user_lxc(self, app_name):
        ansible_runner.run_command(executable_cmd='ansible', cmdline_args=[app_name, '-m', 'import_role',
                                                                                  '-a', "name=technohouser.ansible",
                                                                                  '-e', self.app_path] + VARS +
                                                                                  ['--user','ansible'])

    def setup_lxc(self,app_name):
        self.create_lxc(app_name)
        self.dump_inventory()
        self.bootstrap_lxc(app_name)
        self.ansible_user_lxc(app_name)

    def setup_playbook(self,app_name):
        ansible_runner.run_command(executable_cmd='ansible-playbook',
                                   cmdline_args=[find_playbook(app_name)] + VARS + ['--user','ansible'])