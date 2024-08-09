import unittest

from utils.inventory import ansible_inventory


class TestAnsibleInventory(unittest.TestCase):

  def setUp(self):
    pass

  def test_inventory(self):
    host_vars = ansible_inventory.get_host_vars("lxc")
    assert host_vars is not None
    assert isinstance(host_vars, dict)
    assert len(host_vars) > 0

  def test_inventory_all(self):
    host_vars = ansible_inventory.get_host_vars()
    assert host_vars is not None
    assert isinstance(host_vars, list)
    assert len(host_vars) > 0
    for host in host_vars:
      assert host is not None
      assert len(host.vars) > 0
