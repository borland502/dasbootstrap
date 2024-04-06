import unittest, pytest
from dasbootstrap.utils import *
from xdg_base_dirs import *
from pathlib import Path

TEST_PATH: Path = Path.joinpath(xdg_data_home(), 'dasbootstrap/dasbootstrap/tests/resources')

class UtilsTestCase(unittest.TestCase):

    def test_find_yaml_files(self):
        yaml_files = find_yaml_files(TEST_PATH)
        self.assertEqual(3, len(yaml_files))


if __name__ == '__main__':
    unittest.main()
