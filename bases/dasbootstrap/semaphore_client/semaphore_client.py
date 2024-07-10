"""Client module for the Ansible Semaphore Api project."""

from pydantic import StrictInt, StrictStr
from semaphore_api.api.authentication_api import AuthenticationApi
from semaphore_api.api.project_api import ProjectApi
from semaphore_api.api.projects_api import ProjectsApi
from semaphore_api.api_client import ApiClient, ApiResponse
from semaphore_api.configuration import Configuration
from semaphore_api.models.access_key import AccessKey
from semaphore_api.models.access_key_request import AccessKeyRequest
from semaphore_api.models.inventory import Inventory
from semaphore_api.models.inventory_request import InventoryRequest
from semaphore_api.models.login import Login
from utils.inventory import ansible_inventory


class SemaphoreActions:
    """Basic client adapter for the Ansible Semaphore Api project:
    https://github.com/nchekwa/ansible-semaphore-api/tree/main.
    """

    def __init__(self):
        """:rtype: object"""
        _host_vars = ansible_inventory.get_host_vars("semaphore")
        _host = _host_vars["proxmox_hostname"] + "." + _host_vars["proxmox_searchdomain"]
        _port = _host_vars["semaphore_port"]
        _protocol = _host_vars["semaphore_protocol"]

        _endpoint = f"{_protocol}://{_host}:{_port}/api"
        self.semaphore_config = Configuration(
            host=_endpoint,
            username=_host_vars["semaphore_admin"],
            password=_host_vars["semaphore_token"],
            access_token=_host_vars["semaphore_access_token"],
        )
        self.semaphore_client = ApiClient(configuration=self.semaphore_config)
        self.semaphore_instance = AuthenticationApi(api_client=self.semaphore_client)
        self.auth_call = Login(auth=self.semaphore_config.username, password=self.semaphore_config.password)
        self.all_vars = ansible_inventory.get_host_vars()
        self.project_api = ProjectApi(api_client=self.semaphore_client)
        self._sort_default: StrictStr = StrictStr("name")
        self._order_default: StrictStr = StrictStr("asc")
        self._project_id_default: StrictInt = StrictInt(1)

    # TODO: Refresh host_vars

    def connect(self):
        """Initialize the semaphore client and initialize."""
        login: ApiResponse = self.semaphore_instance.auth_login_post_with_http_info(self.auth_call)
        api_cookie = login.headers["Set-Cookie"]
        self.semaphore_client.cookie = api_cookie
        # TODO: Reinitialize if cookie expires

    def get_projects(self):
        """Get all projects listed in Semaphore application."""
        return ProjectsApi(self.semaphore_client).projects_get()

    # TODO: Project id lookup
    def from_ansible_inventory(self, hostname: str) -> InventoryRequest:
        """Create inventory request object from hostname."""
        # TODO: Handle Groups
        # TODO: Handle exceptions
        # TODO: Don't duplicate inventory with the same name
        ans_vars = ansible_inventory.get_host_vars(hostname=hostname)
        # TODO: Dump ansvars to inventory
        return InventoryRequest.from_dict(
            {
                "name": ans_vars["pve_hostname"],
                "project_id": 1,
                "inventory": str(ans_vars),
                "ssh_key_id": self.find_ssh_key(),
                "become_key_id": self.find_ssh_key(),
                "type": "static-yaml",
            }
        )

    def delete_inventory_for_hostname(self, hostname: str, projectid: int) -> None:
        """Delete 1..N inventory with the same name as the host in a given project."""
        strict_proj_id = StrictInt(projectid)
        proj_inventory: list[Inventory] = [
            inventory
            for inventory in self.project_api.project_project_id_inventory_get(
                project_id=strict_proj_id, sort=self._sort_default, order=self._order_default
            )
            if inventory.name == hostname
        ]

        for inventory in proj_inventory:
            self.project_api.project_project_id_inventory_inventory_id_delete(
                project_id=inventory.project_id, inventory_id=inventory.id
            )

    def find_ssh_key(self, project_id=1, key_name="Ansible Service Key") -> AccessKey | None:
        """:type project_id: Annotated[StrictInt, Field(description="Project ID")],
        :type key_name: str
        """
        ssh_keys = self.project_api.project_project_id_keys_get(
            project_id=project_id, key_type="ssh", sort=self._sort_default, order=self._order_default
        )
        for key in ssh_keys:
            if key_name == key.name:
                return key
        return None

    def create_key(self, project_id: StrictInt = 1, access_key: AccessKeyRequest = None):
        """Create ssh key in Semaphore project."""
        return self.project_api.project_project_id_keys_post(project_id=project_id, access_key=access_key)

    # TODO: Simply have to generate using the ansible inventory dump command and upload the resulting yaml
    def create_inventory(self, hostname: str, project_id: StrictInt = 1) -> Inventory:
        """Create inventory in Semaphore project."""
        return self.project_api.project_project_id_inventory_post(
            project_id=project_id, inventory=self.from_ansible_inventory(hostname=hostname)
        )


if __name__ == "__main__":
    semaphore_client = SemaphoreActions()
    semaphore_client.connect()
