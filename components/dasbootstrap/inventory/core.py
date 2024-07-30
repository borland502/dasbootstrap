from __future__ import annotations

import re
from collections.abc import Hashable
from functools import cached_property
from pathlib import Path

import xdg_base_dirs
from ansible.inventory.group import Group
from cache_decorator import Cache

from components.dasbootstrap.resources.paths import Directories, Inventory
from components.dasbootstrap.resources.paths import Inventory as inv_sources
from components.dasbootstrap.ansible.core import Actions

from ansible.inventory.host import Host
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.plugins.loader import init_plugin_loader
from ansible.vars.manager import VariableManager
import ansible_runner


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

  def get_dataloader(self):
    return self._get_dataloader()


class KitchenSinkInventory:

  cache_dir = xdg_base_dirs.xdg_cache_home() / "ansible/inventory.pkl"
  ignore_args = tuple("self")

  def __init__(self):
    # self._nmap_hosts = self._load_hosts(InventorySource(source=inv_sources.DYNAMIC_NMAP))
    # self._proxmox_hosts = self._load_hosts(InventorySource(source=inv_sources.DYNAMIC_PROXMOX))
    self._static_hosts = self._load_hosts(InventorySource(source=inv_sources.STATIC_HOSTS_YAML))

  def _load_hosts(self, inv_src: InventorySource) -> list[Host]:
    inventory = inv_src.get_inventory_manager()
    var_manager = inv_src.get_variable_manager()

    hosts: list[Host] = inventory.get_hosts()
    for host in hosts:
      host.vars = var_manager.get_vars(host=host)

    return hosts

  def host(self, hostname: str) -> Host:

    hosts = [host for host in self._static_hosts if host.name == hostname]
    if hosts:
      return hosts[0]

  @Cache(cache_dir=str(cache_dir))
  def static_hosts(self) -> list[Host]:
    return self._static_hosts
