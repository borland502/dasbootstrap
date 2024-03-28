import unittest
from unittest.mock import patch
from pathlib import Path
from xdg_base_dirs import xdg_data_home

import codecs

import yaml

from ansible.parsing.yaml.loader import AnsibleLoader
from ansible.parsing.yaml.dumper import AnsibleDumper
from ansible.plugins.cache import BaseFileCacheModule
from ansible_actions.ansible_actions import Actions, Paths

class TestActions(unittest.TestCase):
    actions = Actions()

    def test_path_constants(self):
        paths = Paths()

        # Assert each path is a fully qualified path
        self.assertEqual(paths.PROOT, Path.joinpath(xdg_data_home(), 'dasbootstrap'))
        self.assertEqual(paths.PROOT, Path.joinpath(Path.home(), Path('.local/share/dasbootstrap')))
        self.assertEqual(paths.SCROOT, Path.joinpath(Path.home(),'.local/share/dasbootstrap/bin'))
        self.assertEqual(paths.LROOT, Path.joinpath(Path.home(),'.local/share/dasbootstrap/lib'))
        self.assertEqual(paths.AHOME, Path.joinpath(Path.home(), '.ansible'))
        self.assertEqual(paths.CHOME, Path.joinpath(Path.home(), '.ansible/collections'))
        self.assertEqual(paths.RHOME, Path.joinpath(Path.home(), '.ansible/roles'))
        self.assertEqual(paths.IHOME, Path.joinpath(Path.home(), '.ansible/inventory'))
        self.assertEqual(paths.GVHOME, Path.joinpath(Path.home(), '.ansible/inventory/group_vars'))
        self.assertEqual(paths.HVHOME, Path.joinpath(Path.home(), '.ansible/inventory/host_vars'))

    def test_get_inventory(self):
        inventory = self.actions.dump_inventory()

        # Assertions
        self.assertIsNotNone(inventory, "Inventory should not be None")
        self.assertTrue(yaml.dump(inventory), "Inventory should be valid YAML")
        self.assertGreater(len(inventory), 0, "Inventory should have a size greater than zero")

    def test_update_collections(self):
        test_collections = self.actions.update_collections()

        self.assertIsNotNone(test_collections, "Collections should not be None")
        #TODO: file exists

    def test_update_roles(self):
        test_roles = self.actions.update_roles()

        self.assertIsNotNone(test_roles, "Roles should not be None")
        #TODO: file exists

    # TODO: DNS add/remove
    def test_lxc(self):
        lxc_response = self.actions.create_lxc('lxc')
        self.assertIsNotNone(lxc_response, "LXC should not be None")
        lxc_response = self.actions.bootstrap_lxc('lxc')
        self.assertIsNotNone(lxc_response, "LXC should not be None")
        lxc_response = self.actions.bootstrap_lxc('lxc')
        self.assertIsNotNone(lxc_response, "LXC should not be None")
        lxc_response = self.actions.destroy_lxc('lxc')
        self.assertIsNotNone(lxc_response, "LXC should not be None")


if __name__ == '__main__':
    unittest.main()
