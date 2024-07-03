"""Ansible Commands module."""

import os

import ansible_runner
from utils.paths import find_playbook

from shared.config.resources.paths import Directories, Inventory, Requirements, Variables

INVENTORY: list[str] = ["-i", str(Directories.IHOME)]
# TODO: Validate vars
VARS: list[str] = [
    *INVENTORY,
    *["-e", "@" + str(Variables.ALL_VARS), "-e", "@" + str(Variables.ALL_LXC_VARS), "-e", "@" + str(Variables.ALL_KVM_VARS)],
]


class Actions:
    """Class for interacting with LXC containers using Ansible.

    Provide methods to create, destroy, bootstrap, configure user access,
    and run playbooks for LXC containers.
    """

    def __init__(self, app="lxc"):
        """Initialize the Actions class with the specified application name.

        Args:
            app (str, optional): The application name for the LXC container.
                Defaults to "lxc".
        """
        self.app = app
        self.app_path = f"@{Directories.HVHOME}/{app}.yaml"

        ansible_runner.run_command(
            executable_cmd="ansible-inventory",
            cmdline_args=["all", "--export", "--list", "--yaml", *VARS, "--output", str(Inventory.STATIC_HOSTS)],
        )

    def create_kvm(self):
        """Create a new KVM using the specified application role."""
        ansible_runner.run_command(
            executable_cmd="ansible",
            cmdline_args=[
                "localhost",
                "-m",
                "import_role",
                "-a",
                "name=technohouser.proxmox.create_kvm",
                "-e",
                self.app_path,
                *VARS,
                "--user",
                "root",
            ],
        )

    def create_lxc(self):
        """Create a new LXC container using the specified application role.

        Uses the `technohouser.proxmox.create_lxc` Ansible role to create a new
        LXC container based on the configuration defined in the application's
        playbook.
        """
        ansible_runner.run_command(
            executable_cmd="ansible",
            cmdline_args=[
                "localhost",
                "-m",
                "import_role",
                "-a",
                "name=technohouser.proxmox.create_lxc",
                "-e",
                self.app_path,
                *VARS,
                "--user",
                "root",
            ],
        )

    def destroy_lxc(self):
        """Destroy the specified LXC container using the application role.

        Uses the `technohouser.destroy_xc` Ansible role to destroy the LXC
        container associated with the current application.
        """
        ansible_runner.run_command(
            executable_cmd="ansible",
            cmdline_args=[
                "localhost",
                "-m",
                "import_role",
                "-a",
                "name=technohouser.destroy_lxc",
                "-e",
                self.app_path,
                *VARS,
                "--user",
                "root",
            ],
        )

    def bootstrap_lxc(self, app):
        """Bootstrap the specified LXC container using the application role.

        Uses the `technohouser.bootstrap` Ansible role to bootstrap the
        given LXC container, presumably by installing the required software
        and configuration.
        """
        ansible_runner.run_command(
            executable_cmd="ansible",
            cmdline_args=[
                app,
                "-m",
                "import_role",
                "-a",
                "name=technohouser.dasbootstrap.bootstrap",
                *VARS,
                "-e",
                self.app_path,
                "--user",
                "root",
            ],
        )

    def ansible_user_lxc(self, app):
        """Configure the specified LXC container for Ansible access.

        Uses the `technohouser.ansible` Ansible role to configure the
        given LXC container to allow SSH access by the 'ansible' user, likely
        for further automation.
        """
        ansible_runner.run_command(
            executable_cmd="ansible",
            cmdline_args=[
                app,
                "-m",
                "import_role",
                "-a",
                "name=technohouser.dasbootstrap.ansible",
                "-e",
                self.app_path,
                *VARS,
                "--user",
                "ansible",
            ],
        )

    @classmethod
    def dump_inventory(cls):
        """Convert dynamic inventory sources into a single static host file.

        :return:
        """
        ansible_runner.run_command(
            executable_cmd="ansible-inventory",
            cmdline_args=["all", "--export", "--list", "--yaml", *VARS, "--output", str(Inventory.STATIC_HOSTS)],
        )

    @classmethod
    def update_collections(cls):
        """Update galaxy collections for Dasbootstrap.

        :return:
        """
        ansible_runner.run_command(
            executable_cmd="ansible-galaxy",
            cmdline_args=[
                "collection",
                "install",
                "-r",
                str(Requirements.COLLECTIONS_REQS),
                "--force",
            ],
        )

    @classmethod
    def update_facts(cls):
        """Run the ansible.builtin.setup module against all hosts with the service user."""
        ansible_runner.run_command(
            executable_cmd="ansible",
            cmdline_args=["all", "-m", "setup", *VARS, "--user", "ansible"],
        )

    @classmethod
    def update_roles(cls):
        """Update galaxy roles for Dasbootstrap.

        :return:
        """
        ansible_runner.run_command(
            executable_cmd="ansible-galaxy",
            cmdline_args=["role", "install", "-r", str(Requirements.ROLES_REQS), "--force"],
        )

    @classmethod
    def setup_playbook(cls, app) -> None:
        """Find and execute an ansible playbook using the service user."""
        playbook = find_playbook(app)

        if playbook is None:
            return

        ansible_runner.run_command(
            executable_cmd="ansible-playbook",
            cmdline_args=[playbook, *VARS, "--user", "ansible"],
        )

    @classmethod
    def purge_cache(cls):
        """Erases all files within the ~/.cache/ansible directory."""
        if os.path.exists(Directories.CHOME):
            for filename in os.listdir(Directories.CHOME):
                file_path = os.path.join(Directories.CHOME, filename)
                try:
                    os.remove(file_path)
                except OSError as e:
                    print(f"Error deleting file {file_path}: {e}")
            print(f"Contents of Ansible cache directory '{Directories.CHOME}' erased successfully.")
        else:
            print("Ansible cache directory not found.")
