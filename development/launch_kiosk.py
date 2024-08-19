import fire

from ansible.inventory.host import Host
from components.dasbootstrap.abc.core import DASBootstrap
from components.dasbootstrap.inventory.core import Actions, KitchenSinkInventory


class AnsibleInventory(DASBootstrap):
  def __init__(self):
    self.ansible_actions = Actions()
    self.inventory = KitchenSinkInventory()

  def run(self):
    self.ansible_actions.create_lxc()
    self.ansible_actions.bootstrap_lxc("lxc")
    self.ansible_actions.destroy_lxc()


if __name__ == "__main__":
  fire.Fire(AnsibleInventory)
