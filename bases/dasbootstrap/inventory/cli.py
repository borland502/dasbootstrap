from functools import cached_property
import ipaddress

import fire
import xdg_base_dirs

from components.dasbootstrap.inventory.core import KitchenSinkInventory
from components.dasbootstrap.abc.core import DASBootstrap
from ansible.inventory.host import Host

class ActiveInventory(DASBootstrap):


  @classmethod
  def normalize_hostname(cls, hostname: str) -> str:
    hostname = hostname.lower()
    hostname = hostname.split(".")[0]
    return hostname

  def __init__(self):
    self._active_unique_inventory = {}
    kitchen_sink_inventory = KitchenSinkInventory()
    inventory: list[Host] = kitchen_sink_inventory.merged_inventory
    self._active_unique_inventory = self.preprocess_inventory(inventory)

  def preprocess_inventory(self, inventory: list[Host]) -> dict[str, Host]:
    filtered_inventory: dict[str, Host] = {}
    for host in inventory:
      try:
        if host.name:
          ip = ipaddress.ip_address(host.name)
          # TODO: Craete new host if ip not found in other sources
          print(ip)
      except ValueError:
        # hostname is not from nmap, so normalize and store host
        host.name = self.normalize_hostname(host.name)
        if filtered_inventory.get(f"{host.name}") is None:
          filtered_inventory[f"{host.name}"] = host

        for k in host.vars.keys():
          if k not in filtered_inventory[f"{host.name}"].vars:
            filtered_inventory[f"{host.name}"].vars[k] = host.vars[k]

    return filtered_inventory

  def run(self) -> None:
    print(self._active_unique_inventory)

fire.Fire(ActiveInventory)