"""Client module for the Technitium DNS Server project."""

from pathlib import Path

from tdnss.connection import Connection
from utils.inventory import ansible_inventory

CONFIG_DIR_PATH = Path.home() / ".config" / "tdnss"
CONFIG_FILE_PATH = CONFIG_DIR_PATH / "config.ini"


# def check_config(self):
#   if not Path.is_dir(CONFIG_DIR_PATH):
#     Path.mkdir(CONFIG_DIR_PATH, mode=0o600, exist_ok=True)
#   if not Path.is_file(CONFIG_FILE_PATH):
#     with open(CONFIG_FILE_PATH, "x") as config_file:


class TechnitiumActions:
  """Basic adapter using the https://codeberg.org/JulioLoayzaM/tdnss TDNSS project."""

  def __init__(self):
    """Initialize the client using the api against the Technitium Server."""
    _host_vars = ansible_inventory.get_host_vars("technitiumdns")
    self._host = _host_vars["proxmox_hostname"] + "." + _host_vars["pve_lxc_searchdomain"]
    self._port = _host_vars["technitiumdns_port"]
    self._protocol = _host_vars["technitiumdns_protocol"]
    self._endpoint = f"{self._protocol}://{self._host}:{self._port}"
    self.username = _host_vars["technitiumdns_user"]
    self.password = _host_vars["technitiumdns_password"]
    self.client = Connection(server_url=self._endpoint)
    self._connect()

  def _connect(self):
    """Initialize client and connect to the technitium dns server."""
    # technitium_response: ConnectionResponse = self.client.login(username=self.username, password=self.password)
    # Connection.create_api_token(self=self.client, username=self.username, password=self.password,
    #                             token_name="automation", save=True)


if __name__ == "__main__":
  technitium_client = TechnitiumActions()
