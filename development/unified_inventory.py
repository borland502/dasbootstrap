from dasbootstrap.inventory.core import inventory, nmap_hosts
from ansible.inventory.host import Host

import pprint

if __name__ == "__main__":
  hosts, groups = inventory()
  nmap_hosts = nmap_hosts()

  pp = pprint.PrettyPrinter(indent=2)
  pp.pprint(nmap_hosts[9].get_vars())

  # for host in hosts:
  #   facts = host.get_vars()
  #   ip = host.get_vars()["ip"]
  #   print(ip)
