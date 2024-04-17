from paramiko import HostKeys
from plumbum.cmd import ssh_keygen

from shared.config.resources.paths import OperatingSystemFiles


class HostKeysUtils(HostKeys):

    def __init__(self,filename=OperatingSystemFiles.KNOWN_HOSTS):
        super().__init__(filename=filename)

    # noinspection PyStatementEffect
    def remove(self, hostname):
        """Remove a hostkey from the known hosts file.  Does not error if key does not exist"""
        ret_val = self.lookup(hostname)

        if ret_val is not None:
            ssh_keygen["-f", "/home/ansible/.ssh/known_hosts", "-R", hostname]
