"""SSH Utilities Module."""

from __future__ import annotations

from dasbootstrap.resources.paths import OperatingSystemFiles
from paramiko import HostKeys
from plumbum.cmd import ssh_keygen


class HostKeysUtils(HostKeys):
  """Utility class for managing SSH host keys in the known_hosts file.

  This class inherits from `HostKeys` (assumed functionality) and provides additional
  methods for interacting with host keys in the known_hosts file.

  Attributes:
      filename (str, optional): The path to the known_hosts file. Defaults to
          `OperatingSystemFiles.KNOWN_HOSTS`.
  """

  def __init__(self, filename=OperatingSystemFiles.KNOWN_HOSTS):
    """Initializes the HostKeysUtils object with the specified filename.

    Args:
        filename (str, optional): The path to the known_hosts file. Defaults to
            `OperatingSystemFiles.KNOWN_HOSTS`.

    This constructor calls the superclass constructor (`HostKeys.__init__`)
    to handle any base class initialization, and then sets the `filename`
    attribute for this class.
    """
    super().__init__(filename)

  def remove(self, hostname):
    """Removes a host key from the known_hosts file.

    Args:
        hostname (str): The hostname of the key to remove.

    This method attempts to remove the specified `hostname` from the known_hosts
    file. It first checks if the key exists using `self.lookup(hostname)`. If the
    key is found, it executes the `ssh-keygen` command with the following arguments:

    - `-f`: Specifies the known_hosts file path.
    - `-R`: Instructs `ssh-keygen` to remove the key for the given hostname.

    **Note:** This method does not explicitly raise an error if the key is not found.
    It's recommended to check the return value of `self.lookup(hostname)` before
    calling `remove` to handle the case where the key doesn't exist.

    Returns:
        None
    """
    ret_val = self.lookup(hostname)

    if ret_val is not None:
      # noinspection PyStatementEffect
      ssh_keygen["-f", "/home/ansible/.ssh/known_hosts", "-R", hostname]
