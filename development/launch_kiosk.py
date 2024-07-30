import fire
from ansible.inventory.host import Host

from components.dasbootstrap.inventory.core import Actions, KitchenSinkInventory
from components.dasbootstrap.abc.core import DASBootstrap


class AnsibleInventory(DASBootstrap):

  def __init__(self):
    self.ansible_actions = Actions()
    self.inventory = KitchenSinkInventory()

  def run(self):
    host: Host = self.inventory.host("lxc")
    if host:
      self.ansible_actions.create_lxc()

if __name__ == '__main__':
    fire.Fire(AnsibleInventory)