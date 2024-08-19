import ipaddress
import unittest

from ansible.inventory.host import Host
from bases.dasbootstrap.inventory.cli import ActiveInventory


class TestInventory(unittest.TestCase):
  """Run functional tests against a real environment"""

  def setUp(self):
    self.inventory: dict[str, Host] = ActiveInventory().inventory

  def testInventoryPresent(self):
    assert len(self.inventory) > 0

  def testKeys(self):
    assert sorted(self.inventory.keys()) == sorted(self.inventory.keys())
    # The key should be a hostname without a domain unless it is an ip address
    for key in self.inventory.keys():
      assert key.find(".") == -1 or ipaddress.ip_address(key).is_private

  def testValues(self):
    for value in self.inventory.values():
      assert isinstance(value, Host)
      assert value.name
      assert value.vars
      assert value.groups
      assert value.address
      assert len(value.vars) > 0
      assert len(value.groups) > 0
