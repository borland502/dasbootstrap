"""Generates a static fake inventory list for Ansible tests

@Author abhinav1107
# https://gist.githubusercontent.com/abhinav1107/471df18abf140dc816902a249be419cf/raw/f330ae9159c06af935d363ca0199b02902faec2b/ansible-random-inventory-generator.py
"""

import argparse
import random
import string

from ipaddr import IPNetwork
from netaddr import *

CHAR_LIST = list(string.ascii_lowercase)


def word_generator(word_length):
  random_word = "".join(random.choice(CHAR_LIST) for _ in range(word_length))
  return random_word


def inventory_generator(my_network, host_prefix, inventory_file_path):
  region_suffix_list = ["1a", "1b", "1c", "1d", "1e"]
  group_line_range = 0
  counter = 0
  with open(inventory_file_path, "w") as f:
    for each_ip in IPNetwork(my_network).iter_hosts():
      ip = str(each_ip)
      instance_name1 = word_generator(5)
      instance_name2 = word_generator(7)
      instance_number_suffix = random.randrange(30)
      instance_zone_suffix = random.choice(region_suffix_list)
      instance_final_name = (
        host_prefix
        + "-"
        + instance_name1
        + "-"
        + instance_name2
        + "-"
        + str(instance_number_suffix)
        + "-"
        + instance_zone_suffix
        + "\n"
      )
      current_line = "%s ht_name=%s" % (ip, instance_final_name)

      if group_line_range == 0:
        current_line = "[all]\n\n" + "[" + word_generator(7) + "]\n" + current_line
        group_line_range = random.randrange(3, 30)
      if group_line_range == counter:
        counter = 0
        group_line_range = random.randrange(3, 30)
        current_line = "\n\n[" + word_generator(7) + "]\n" + current_line
      else:
        counter += 1

      f.write(current_line)


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="A simple python script to generate ansible inventory")
  parser.add_argument("-n", "--network", help="Your IP Address Network. Defaults to: 192.168.1.0/24", default="192.168.1.0/24")
  parser.add_argument("-p", "--prefix", help="Prefix for each host name. Defaults to: dev", default="dev")
  parser.add_argument(
    "-P", "--path", help="Path of the inventory file. Defaults to: ./my_ansible_hosts", default="my_ansible_hosts"
  )
  args = parser.parse_args()

  inventory_generator(args.network, args.prefix, args.path)
