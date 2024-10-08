"""Base resources module for the Proxmoxer API.

https://github.com/ansible-collections/community.general/blob/d2d7deb4ecb978dd21a68b4ebd372da891ee3029/plugins/module_utils/proxmox.py#L12
"""

from __future__ import annotations

import logging

from proxmoxer import ProxmoxAPI


class Resources:
  def __init__(self, proxmox: ProxmoxAPI):
    self.proxmox = proxmox
    self.log: logging.Logger = logging.getLogger("Resources")

  def get_nodes(self):
    try:
      return list(self.proxmox.nodes.get())
    except Exception as e:
      self.log.error(msg=f"Unable to retrieve Proxmox VE nodes: {e}")

  def get_node(self, node):
    try:
      return next(n for n in self.proxmox.nodes.get() if n["node"] == node)
    except Exception as e:
      self.log.error(msg=f"Unable to retrieve Proxmox VE node: {e}")

  def get_vms(self) -> list:
    return list(self.proxmox.cluster.resources.get(type="vm"))

  def get_vm(self, vmid, ignore_missing=False):
    global vms
    try:
      vms = [vm for vm in self.proxmox.cluster.resources.get(type="vm") if vm["vmid"] == int(vmid)]
    except Exception as e:
      vms = None
      self.log.error(msg=f"Unable to retrieve list of VMs filtered by vmid {vmid}: {e}")
    if vms:
      return vms[0]
    else:
      if ignore_missing:
        return None
      self.log.error(msg=f"VM with vmid {vmid} does not exist in cluster")
      return None

  def get_pool(self, poolid):
    """Retrieve pool information
    :param poolid: str - name of the pool
    :return: dict - pool information.
    """
    try:
      return self.proxmox.pools(poolid).get()
    except Exception as e:
      self.log.error(msg=f"Unable to retrieve pool {poolid} information: {e}")

  def get_storages(self, type):
    """Retrieve storages information
    :param type: str, optional - type of storages
    :return: list of dicts - array of storages.
    """
    try:
      return self.proxmox.storage.get(type=type)
    except Exception as e:
      self.log.error(msg=f"Unable to retrieve storages information with type {type}: {e}")

  def get_storage_content(self, node, storage, content=None, vmid=None):
    try:
      return self.proxmox.nodes(node).storage(storage).content().get(content=content, vmid=vmid)
    except Exception as e:
      self.log.error(msg=f"Unable to list content on {node}, {storage} for {content} and {vmid}: {e}")
