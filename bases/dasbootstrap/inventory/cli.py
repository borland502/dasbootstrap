import ipaddress
from functools import cached_property

import fire
from dns import reversename, resolver
from dns.name import Name
from dns.resolver import NXDOMAIN

from components.dasbootstrap.inventory.core import KitchenSinkInventory
from components.dasbootstrap.abc.core import DASBootstrap
from ansible.inventory.host import Host


class ActiveInventory(DASBootstrap):

  def __init__(self):
    kitchen_sink_inventory = KitchenSinkInventory()
    inventory: list[Host] = kitchen_sink_inventory.merged_inventory
    self._active_unique_inventory = self._preprocess_inventory(inventory)

  @classmethod
  def _normalize_hostname(cls, hostname: str) -> str | None:
    ip: None = None
    try:
      ip: str = str(ipaddress.ip_address(hostname)).strip()
      name: Name = reversename.from_address(ip)
      resolved_name: str = str(resolver.resolve(name, "PTR")[0])

      if resolved_name.endswith("."):
        hostname = resolved_name[:-1]

    except NXDOMAIN:
      return ip

    except ValueError:
      pass

    if hostname.startswith("*"):
      return None

    hostname = hostname.lower()
    hostname = hostname.split(".")[0]
    return hostname

  @classmethod
  def _filter_duplicates(cls, filtered_inventory, host: Host):
    # We are only interested in sources that provide Host objects
    if host is None or not isinstance(host, Host):
      return None

    # hostname is not from nmap, so normalize and store host
    host.name = cls._normalize_hostname(host.name)
    if host.name is None:
      return None

    if filtered_inventory.get(f"{host.name}") is None:
      filtered_inventory[f"{host.name}"] = host
    for k in host.vars.keys():
      if k not in filtered_inventory[f"{host.name}"].vars:
        filtered_inventory[f"{host.name}"].vars[k] = host.vars[k]

  @classmethod
  def _host_generator(cls, inventory: list[Host]) -> Host:
    yield inventory.pop()

  def _preprocess_inventory(self, inventory: list[Host]) -> dict[str, Host]:
    filtered_inventory: dict[str, Host] = {}

    for host in inventory:
      self._filter_duplicates(filtered_inventory, host)

    return filtered_inventory

  @cached_property
  def inventory(self) -> dict[str, Host]:
    return self._active_unique_inventory

  def run(self) -> None:
    print(self.inventory)


fire.Fire(ActiveInventory)
