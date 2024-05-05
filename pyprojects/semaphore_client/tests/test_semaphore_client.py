import pytest
from pydantic import StrictInt,StrictStr
from semaphore_api.models.inventory import Inventory
from semaphore_api.api.project_api import InventoryRequest, Project

from ..semaphore_client import SemaphoreActions


@pytest.fixture
def get_semaphore_client() -> SemaphoreActions:
  semaphore_client = SemaphoreActions()
  semaphore_client.initialize()
  yield semaphore_client


@pytest.fixture()
def get_inventory_request(get_semaphore_client) -> InventoryRequest:
  inventory_req = get_semaphore_client.from_ansible_inventory("lxc")
  assert inventory_req is not None
  yield inventory_req
  projectid=StrictInt(1)
  hostname=StrictStr("lxc")
  get_semaphore_client.delete_inventory_for_hostname(hostname=hostname, projectid=projectid)

@pytest.fixture()
def get_projects(get_semaphore_client) -> list[Project]:
    projects = get_semaphore_client.get_projects()
    yield projects

class TestSemaphoreClient:

  def test_client_init(self, get_semaphore_client):
    assert get_semaphore_client.semaphore_client.cookie is not None

  def test_get_projects(self, get_projects: list[Project]):
    assert get_projects is not None
    assert len(get_projects) > 0

  def test_create_inventory(self, get_inventory_request):
    assert get_inventory_request.name == "lxc"
