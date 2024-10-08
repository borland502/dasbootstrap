"""Info module for Proxmoxer API."""

from __future__ import annotations

from proxmoxer import ProxmoxAPI

from proximate_utils.resources import Resources


class Info(Resources):
  def __init__(self, proxmox: ProxmoxAPI):
    super().__init__(proxmox)

  def version(self) -> str:
    try:
      return self.proxmox.version.get()
    except Exception as e:
      self.log.error(msg=f"Unable to retrieve Proxmox VE version: {e}")

  def get_nextvmid(self):
    try:
      return self.proxmox.cluster.nextid.get()
    except Exception as e:
      self.log.error(msg=f"Unable to retrieve next free vmid: {e}")

  def get_vmid(self, name, ignore_missing=False):
    vms = []
    try:
      vms = [vm["vmid"] for vm in self.proxmox.cluster.resources.get(type="vm") if vm.get("name") == name]
    except Exception as e:
      vms = None
      self.log.error(msg=f"Unable to retrieve list of VMs filtered by name {name}: {e}")
    if not vms:
      if ignore_missing:
        return None
      self.log.error(msg=f"No VM with name {name} found")
      return None
    elif len(vms) > 1:
      self.log.error(msg=f"Multiple VMs with name {name} found, provide vmid instead")
      return None
    else:
      return vms[0]

  def api_task_ok(self, node, taskid):
    try:
      status = self.proxmox.nodes(node).tasks(taskid).status.get()
      return status["status"] == "stopped" and status["exitstatus"] == "OK"
    except Exception as e:
      self.log.error(msg=f"Unable to retrieve API task ID from node {node}: {e}")
