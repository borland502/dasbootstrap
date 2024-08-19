"""Dasbootstrap base core module."""

from typer import Option, Typer

from dasbootstrap.ansible.core import Actions, Plays
from dasbootstrap.resources.paths import OperatingSystemFiles
from dasbootstrap.ssh import HostKeysUtils


def create_kvm(
  app_name: str = Option("kvm", help="Virtual machine to manage (defaults to kvm)"),
):
  """Create and set up a new KVM using debian by default."""
  actions = Actions(app_name)
  actions.create_kvm()
  # preemptively delete the host key
  HostKeysUtils(filename=OperatingSystemFiles.KNOWN_HOSTS).remove(app_name)
  Actions.dump_inventory()
  actions.bootstrap_lxc(app_name)
  actions.ansible_user_lxc(app_name)


def create_lxc(
  app_name: str = Option("lxc", help="Application to manage (defaults to lxc)"),
):
  """Create and set up a new LXC container, installing favorites, and creating a service user."""
  actions = Actions(app_name)
  actions.create_lxc()
  # preemptively delete the host key
  HostKeysUtils(filename=OperatingSystemFiles.KNOWN_HOSTS).remove(app_name)
  Actions.dump_inventory()
  actions.bootstrap_lxc(app_name)
  actions.ansible_user_lxc(app_name)
  # if a playbook exists with the app_name then run it
  actions.setup_playbook(app_name)


def destroy(
  app_name: str = Option("lxc", help="Application to manage (defaults to lxc)"),
):
  """Destroy an existing LXC container."""
  actions = Actions(app_name)
  actions.destroy_lxc()


def update_facts():
  """Update facts for all managed hosts."""
  Actions.update_facts()


def update_containers(
  user: str = Option("user", help="Ansible user to run playbook under"),
):
  """Update Ansible containers from requirements."""
  Plays.update_containers(user=user)


def update_collections():
  """Update Ansible collections from requirements."""
  Actions.update_collections()


def dump_inventory():
  """Dump the inventory to hosts.yaml."""
  Actions.dump_inventory()


def update_roles():
  """Update Ansible roles from requirements."""
  Actions.update_roles()
