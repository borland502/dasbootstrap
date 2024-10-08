import tempfile
import unittest
from pathlib import Path

from dasbootstrap.inventory.core import InventorySource

from .inventory_generator import inventory_generator


class TestInventory(unittest.TestCase):
  def setUp(self):
    with tempfile.TemporaryDirectory(delete=False) as tmpdir:
      temp_inventory_file = str(Path(tmpdir).joinpath("hosts.ini"))
      inventory_generator(my_network="192.168.10.0/28", host_prefix="test", inventory_file_path=temp_inventory_file)
      assert temp_inventory_file is not None
      self._static_host = temp_inventory_file
      source = Path(self._static_host)
      self.inventory_source = InventorySource(basedir=source.parent, source=str(source))

  # TODO: cache needs to be a configurable parameter
  def test_inv_mgr(self):
    assert self.inventory_source is not None
    inv_mgr = self.inventory_source.get_inventory_manager()
    assert inv_mgr is not None
    self.assertEqual(14, len(inv_mgr.hosts))
    # always should be at least 2, all and ungrouped
    self.assertLessEqual(2, len(inv_mgr.groups))
    assert inv_mgr.groups.get("all") is not None
    assert inv_mgr.groups.get("ungrouped") is not None
