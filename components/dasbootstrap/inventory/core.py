from __future__ import annotations

import dataclasses
import datetime
import re
from collections.abc import Hashable
from functools import cached_property
from pathlib import Path

import xdg_base_dirs
from ansible.inventory.group import Group

from components.dasbootstrap.resources.paths import Directories, Inventory
from components.dasbootstrap.resources.paths import Inventory as inv_sources
from components.dasbootstrap.ansible.core import Actions
from cachier import cachier, set_default_params

from ansible.inventory.host import Host
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.plugins.loader import init_plugin_loader
from ansible.vars.manager import VariableManager
import ansible_runner

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

  @property
  def source(self):
    return self.sources


class KitchenSinkInventory:

  cache_dir = xdg_base_dirs.xdg_cache_home() / "dasbootstrap"
  ignore_args = tuple("self")

  def __init__(self):
    set_default_params(
      stale_after=datetime.timedelta(days=1),
      cache_dir=self.cache_dir,
    )

  @cachier(allow_none=True)
  def _gather_facts(self):
    Actions.gather_facts()

  @cachier()
  def _proxmox_source(self) -> list[Host]:
    inv_source = InventorySource(source=inv_sources.DYNAMIC_PROXMOX)
    return self._load_hosts(inv_source, inv_source.get_inventory_manager(), inv_source.get_variable_manager())

  @cachier()
  def _static_source(self) -> list[Host]:
    inv_source = InventorySource(source=inv_sources.STATIC_HOSTS_TOML)
    return self._load_hosts(InventorySource(source=inv_sources.STATIC_HOSTS), inv_source.get_inventory_manager(), inv_source.get_variable_manager())

  @cachier()
  def _ldap_source(self) -> list[Host]:
    inv_source = InventorySource(source=inv_sources.DYNAMIC_LDAP)
    return self._load_hosts(InventorySource(source=inv_sources.DYNAMIC_LDAP), inv_source.get_inventory_manager(), inv_source.get_variable_manager())

  @cachier()
  def _nmap_source(self) -> list[Host]:
    inv_source = InventorySource(source=inv_sources.DYNAMIC_NMAP)
    return self._load_hosts(InventorySource(source=inv_sources.DYNAMIC_NMAP), inv_source.get_inventory_manager(), inv_source.get_variable_manager())

  @classmethod
  def _load_hosts(cls, inv_src: InventorySource, inv_mgr: InventoryManager, var_mgr: VariableManager) -> list[Host]:

    hosts: list[Host] = inv_mgr.get_hosts()
    for host in hosts:
      host.vars = var_mgr.get_vars(host=host)

      # if cls._merged_hosts.get(host.name) is None:
      #   cls._merged_hosts[host.name] = host
      # else:
      #   host.vars.update({k:v for (k,v) in host.vars if cls._merged_hosts[host.name].vars.get(k) is None })
    return hosts

  @cached_property
  def static_hosts(self) -> list[Host]:
    Actions.dump_inventory()
    return self._load_hosts(self._static_source)

  @cached_property
  def proxmox_hosts(self) -> list[Host]:
    return self._proxmox_source

  @cached_property
  def nmap_hosts(self) -> list[Host]:
    return self._nmap_source

  @cached_property
  def ldap_hosts(self) -> list[Host]:
    return self._ldap_source

  @property
  def merged_inventory(self) -> list[Host]:
    merged_inventory: list[Host] = self.proxmox_hosts()
    merged_inventory.extend(self.ldap_hosts())
    merged_inventory.extend(self.nmap_hosts())
    return merged_inventory