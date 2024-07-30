#!/usr/bin/env python3

import pprint
import string

from components.dasbootstrap.inventory.core import KitchenSinkInventory

if __name__ == "__main__":
  inventory = KitchenSinkInventory()

  pp = pprint.PrettyPrinter(indent=2)
  for p_host in inventory.proxmox_hosts:
    for n_host in inventory.nmap_hosts:
      p_host_vars = p_host.get_vars()
      n_host_vars = n_host.get_vars()
      if str(p_host_vars.get("ansible_default_ipv4")['address']) == n_host.address:
        print(p_host_vars.get("inventory_hostname"))
      elif p_host_vars.get("inventory_hostname_short") == n_host_vars.get("inventory_hostname_short"):
        print(p_host_vars.get("inventory_hostname"))


  # pp.pprint(inventory.nmap_hosts)

  # for host in hosts:
  #   facts = host.get_vars()
  #   ip = host.get_vars()["ip"]
  #   print(ip)
