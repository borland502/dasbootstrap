# Singleton pattern for "private" methods
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.plugins.loader import init_plugin_loader
from ansible.vars.manager import VariableManager

from dasbootstrap.paths.resources.paths import Directories


def _get_dataloader(basedir=Directories.AHOME):
  init_plugin_loader()
  loader = DataLoader()
  loader.set_basedir(basedir)
  return loader


def _get_inventory_manager(loader: DataLoader | None = None, sources: str | None = None):
  if loader is None:
    loader = _get_dataloader()

  if sources is None:
    sources = os.path.join(Directories.AHOME, "inventory")

  return InventoryManager(loader, sources)


def _get_variable_manager(loader: DataLoader | None = None, inventory: InventoryManager | None = None):
  if loader is None:
    loader = _get_dataloader()

  if inventory is None:
    inventory = _get_inventory_manager()

  return VariableManager(loader, inventory)


# TODO: Add host programmatically rather than voiding cache on new proxmox container if absent


# TODO: Transform this into a class with singletons
def get_host_vars(
  hostname: str | None = None, inventory: InventoryManager | None = None, var_manager: VariableManager | None = None
) -> dict | list[dict]:
  """Get ansible variables for hostname or a list of all hosts with their variables."""
  if inventory is None:
    inventory = _get_inventory_manager()

  if var_manager is None:
    var_manager = _get_variable_manager()

  """Return either the vars for a specific host, or a list of hosts with vars."""
  if hostname is None:
    hosts: list[dict] = inventory.get_hosts()
    for host in hosts:
      # prime the cache of host_vars, either internal or persistent
      var_manager.get_vars(host=host, include_hostvars=True, use_cache=True)
    return hosts

  host = inventory.get_host(hostname)
  return var_manager.get_vars(host=host, use_cache=True)
