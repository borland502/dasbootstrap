Role `cielito.proxmox.users_and_groups`
=========

The Ansible role `cielito.proxmox.users_and_groups` aims to manage te Proxomox users (linked to pam accounts) as well as groups and Proxomox permissions.

This role is derivated from [`udelarinterior.proxmox_users`](https://galaxy.ansible.com/udelarinterior/proxmox_users) ans follows the same evolution that [`udelarinterior.users`](https://galaxy.ansible.com/udelarinterior/users) role, when migrating to [`cielito.system` collection](https://galaxy.ansible.com/cielito/system).
 an can be used with it to create PAM accounts and associated Proxmox users.

The role can worthly be used in conjunction with [`cielito.system.users_and_groups` role](https://git.interior.edu.uy/cielito/system/tree/7-motd-role/roles/users_and_groups) to create the system users and their proxmox associated users, sourcing users' and groups' data from the same structures.

Requirements
------------

This role has to be ran against a Proxmox server (phisical or virtual) or one or several nodes of Proxmox cluster.

Role Variables
--------------

### Users' data

```yaml
pve_users_data:

  user1:
      name: User One
      email: user1@domain.org
      firstname: User
      lastname: One

    user2:
      name: User Two
      expire: 8600   # in seconds

    user3:
      name: User Three
      enable: 0

```
`pve_users_data` structure is somehow compatible with [`cielito_users_data` variable](https://git.interior.edu.uy/cielito/system/tree/7-motd-role/roles/users_and_groups#extended-users-data-reference) of [`cielito.system.users_and_groups`](https://git.interior.edu.uy/cielito/system/tree/7-motd-role/roles/users_and_groups) role. While they don't have the same set of attributes, both `cielito.system.users_and_groups` and `cielito.proxmox.users_and_groups` can be stored in the same variable of a whole group of hosts.

### Cluster's list of users

Optionnally, the role proposes the variables `pve_host_username_list` and `pve_global_username_list` to filter the set of proxmox users to be created, updated or deleted:
```yaml
pve_cluster_username_list:
- user1
- user2

```
This variable is usful to manage several proxmox clusters, or to limit proxmox acces to a subset of your whole list of users, when the structure is used for other purposes, such as hosts system users.

`pve_global_username_list` is intended to separate system users such as root or ansible controller user, and is useful if you manage several clusters, for these users that should not change.

### Groups' data

`pve_groups` is the structure of the groups' data:

```yaml
pve_groups:
  group1:
    comment: Group One
    members:
    - user1
    - user2
  group2:
    comment: Group Two
    members:
    - user2
    - user3
```
On the same way, this variable is compatible with [`cielito_groups` variable](https://git.interior.edu.uy/cielito/system/tree/7-motd-role/roles/users_and_groups#groups-data) of [`cielito.system.users_and_groups`](https://git.interior.edu.uy/cielito/system/tree/7-motd-role/roles/users_and_groups) role.

### Proxmox permissios

`pve_permissions` is the structure of persmissions data. It is a list of the following dict:
```yaml
- path: <proxmox_datacenter_path>
  user: <user> (and no "group:" defined)
  group: <group> (and no "user:" defined)
  role: <proxmox role>
```
Either the key `user:` or the the key `group:` must be defined, not both.


Dependencies
------------

This role dosen't perform the unix users and groups creation, which are needed. This can be done before in the playbook with the role [`cielito.system.users_and_groups`](https://git.interior.edu.uy/cielito/system/tree/7-motd-role/roles/users_and_groups).

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }

License
-------

GPL-3.0-or-later

Author Information
------------------

(c) 2022 UdelaR Interior, Daniel Viñar Ulriksen, @ulvida
