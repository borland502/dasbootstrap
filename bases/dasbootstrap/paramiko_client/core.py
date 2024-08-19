from paramiko.client import SSHClient
from scp import SCPClient


class Scp:
  def __init__(self, hostname: str, username: str, password: str):
    self.ssh = SSHClient()
    self.ssh.load_system_host_keys()
    self.ssh.connect(hostname, username=username, password=password)

  def __enter__(self):
    return SCPClient(self.ssh.get_transport())
