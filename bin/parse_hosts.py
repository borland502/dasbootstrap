#!/usr/bin/env python
from __future__ import annotations

import yaml
from pydantic import BaseModel
from abc import ABC, abstractmethod

@dataclass
class FileType(strenum.Enum):
  TOML = auto()
  YAML = auto()
  JSON = auto()

class ParseAnsibleInventory(BaseModel):
  """Base Factory class for parsing Ansible inventory files by type."""


  @abstractmethod
  def create_parser(self, filetype: FileType, filename: FilePath) -> ParseAnsibleInventory:
    """Abstract method to parse an Ansible inventory file by type.

    Args:
        filetype (FileType): One of the FileType enum values.
        filename (FilePath, optional): Inventory file path. Defaults to Path.home() / ".ansible/inventory/hosts.toml".
    """
    pass

  def parse_file(self) -> FilePath:
    """Take in a filetype and a filename and return a sqlite database.

    Returns:
        FilePath: SQLite database path.
    """


class TOMLAnsibleInventory(ParseAnsibleInventory):
  """Parses Ansible inventory files in TOML format."""



def parse_ansible_inventory(filename) -> tuple:



def parse_ansible_hosts(filename) -> tuple:
    """Parses an Ansible static hosts file in YAML format and extracts information.

    Args:
        filename: Path to the Ansible static hosts file.

    Returns:
        A dictionary where keys are hostnames and values are dictionaries with keys:
            - ip: IP address of the host (if provided)
            - groups: Comma-separated list of groups the host belongs to
    """
    # TODO: create different methods to slice the data down to groups, hosts, and vars.  Then create a method to store that relationship

    with open(filename) as f:
        try:
            data: dict = yaml.safe_load(f)

            all_groups = data["all"]["children"]

            for group in all_groups:
                hosts: dict = all_groups[group]["hosts"]
                if len(group) > 1:
                    hostvars: dict = all_groups[group]["vars"]

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
