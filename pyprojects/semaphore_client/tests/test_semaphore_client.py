from semaphore_api.models.inventory import Inventory

from ..semaphore_client import SemaphoreActions


class TestSemaphoreClient:

    def test_client_init(self):
        semaphore_client = SemaphoreActions()
        semaphore_client.initialize()

        assert semaphore_client.semaphore_client.cookie is not None

    def test_get_projects(self):
        semaphore_client = SemaphoreActions()
        semaphore_client.initialize()
        projects = semaphore_client.get_projects()

        assert projects is not None
        assert len(projects) > 0

    def test_create_inventory(self):
        semaphore_client = SemaphoreActions()
        semaphore_client.initialize()
        inventory_req = semaphore_client.from_ansible_inventory("lxc")

        assert inventory_req is not None

        inventory: Inventory = semaphore_client.create_inventory("lxc")

        assert inventory is not None
        assert inventory.name == "lxc"
