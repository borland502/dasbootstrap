from __future__ import annotations

import re
from pathlib import Path

from ansible.inventory.host import Host
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.plugins.loader import init_plugin_loader
from ansible.vars.manager import VariableManager

from dasbootstrap.resources.paths import Directories, Inventory as inv_sources


def extract_ips(data: list[Host]):
  """Extracts all valid IP addresses (IPv4) from a list.

  Args:
      data: A list containing mixed elements (strings and IP addresses).

  Returns:
      A list containing only the extracted valid IP addresses.
  """
  ip_pattern = r"((?:\d{1,3}\.){3}\d{1,3})|(?:\d{1,3}\.){3}\d{1,3}-\d{1,3}"
  return [item for item in data if re.match(ip_pattern, item.get_name())]


class InventorySource:
  """InventorySource is a simple abstraction over ansible's complicated inventory plugin system."""
  default_basedir: Path = Path(Directories.IHOME)

  def __init__(self, basedir: Path = default_basedir, source=None):
    """To gain absolute control over merge we accept only one source rather than a directory."""
    self.basedir = basedir
    self.sources = source

  def _get_dataloader(self):
    init_plugin_loader()
    loader = DataLoader()
    loader.set_basedir(str(self.basedir))
    return loader

  def get_inventory_manager(self):
    return InventoryManager(self._get_dataloader(), self.sources)

  def get_variable_manager(self):
    return VariableManager(self._get_dataloader(), self.get_inventory_manager())


def _load_hosts(inv_src: InventorySource) -> list[Host]:
 inventory = inv_src.get_inventory_manager()
 var_manager = inv_src.get_variable_manager()

 hosts: list[Host] = inventory.get_hosts()
 hosts = [host for host in hosts if var_manager.get_vars(host=host, include_hostvars=True)]

 return hosts

def _load_host(inv_src: InventorySource, hostname: str) -> Host:
  inventory = inv_src.get_inventory_manager()
  return inventory.get_host(hostname)

class KitchenSinkInventory:

  def __init__(self):
    self._nmap_source = InventorySource(source=inv_sources.DYNAMIC_NMAP)
    self._proxmox_source = InventorySource(source=inv_sources.DYNAMIC_PROXMOX)
    self._ldap_source = InventorySource(source=inv_sources.DYNAMIC_LDAP)

  @property
  def nmap_hosts(self):
    return _load_hosts(self._nmap_source)

  def nmap_host(self, hostname: str) -> Host:
    return _load_host(self._nmap_source, hostname)

  @property
  def proxmox_hosts(self):
    return _load_hosts(self._proxmox_source)

  def proxmox_host(self, hostname: str):
    return _load_host(self._proxmox_source, hostname)


if __name__ == '__main__':
    kitchenSink = KitchenSinkInventory()
    kitchenSink._process_source()