"""Main module for Dasbootstrap."""


from typer import Option, Typer

from shared.config.resources.paths import OperatingSystemFiles
from shared.utils.ssh import HostKeysUtils

from .ansible_commands import Actions

app = Typer()


@app.command()
def create(app_name: str = Option("lxc", help="Application to manage (defaults to lxc)")):
    """Creates and sets up a new LXC container, installing favorites, and creating a service user"""
    actions = Actions(app_name)
    actions.create_lxc()
    # preemptively delete the host key
    HostKeysUtils(filename=OperatingSystemFiles.KNOWN_HOSTS).remove(app_name)
    Actions.dump_inventory()
    actions.bootstrap_lxc(app_name)
    actions.ansible_user_lxc(app_name)
    # if a playbook exists with the app_name then run it
    actions.setup_playbook(app_name)


@app.command()
def destroy(app_name: str = Option("lxc", help="Application to manage (defaults to lxc)")):
    """Destroys an existing LXC container."""
    actions = Actions(app_name)
    actions.destroy_lxc()


@app.command()
def update_facts():
    """Updates facts for all managed hosts."""
    Actions.update_facts()


@app.command()
def update_collections():
    """Updates Ansible collections from requirements."""
    Actions.update_collections()


@app.command()
def dump_inventory():
    """Dump the inventory to hosts.yaml"""
    Actions.dump_inventory()


@app.command()
def update_roles():
    """Updates Ansible roles from requirements."""
    Actions.update_roles()


if __name__ == "__main__":
    app()
