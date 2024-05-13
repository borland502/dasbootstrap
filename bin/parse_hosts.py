#!/usr/bin/env python


import yaml


def parse_ansible_hosts(filename) -> tuple:
  """
  Parses an Ansible static hosts file in YAML format and extracts information.

  Args:
      filename: Path to the Ansible static hosts file.

  Returns:
      A dictionary where keys are hostnames and values are dictionaries with keys:
          - ip: IP address of the host (if provided)
          - groups: Comma-separated list of groups the host belongs to
  """
  # TODO: create different methods to slice the data down to groups, hosts, and vars.  Then create a method to store that relationship

  with open(filename, "r") as f:
    try:
      data: dict = yaml.safe_load(f)

      all_groups = data['all']['children']

      for group in all_groups.keys():
        hosts:dict = all_groups[group]['hosts']
        if len(group) > 1:
          hostvars:dict = all_groups[group]['vars']

    except yaml.YAMLError as exc:
      print(f"Error parsing YAML file: {exc}")
    return hosts, hostvars

def process_hosts(hosts: dict, hostvars: dict):
  print(hosts)
  print(hostvars)

# Example usage
if __name__ == "__main__":
  hosts_file = "/home/ansible/.ansible/inventory/hosts.yaml"  # Replace with your actual hosts file path
  hosts, hostvars = parse_ansible_hosts(hosts_file)
  process_hosts(hosts, hostvars)
