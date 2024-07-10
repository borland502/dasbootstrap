from dasbootstrap.paths.core import find_yaml_files, find_playbooks, find_hosts
from dasbootstrap.paths.resources.paths import Directories


class TestUtils:

    def test_find_yaml_files(self):
        files = find_yaml_files(Directories.PBROOT)
        for file in files:
            assert isinstance(file, str)
            assert file.endswith("yaml")
        assert len(files) > 0

    def test_find_playbooks(self):
        files = find_playbooks()
        other_files = find_yaml_files(Directories.PBROOT)
        assert len(files) > 0
        assert files == other_files

    def test_find_hosts(self):
        files = find_hosts()
        other_files = find_yaml_files(Directories.HVHOME)
        assert len(files) > 0
        assert files == other_files