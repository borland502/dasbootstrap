#!/usr/bin/env bash
# ansible folder paths
declare -rx ANSIBLE_HOME="${HOME}/.ansible"
declare -rx ANSIBLE_FORKS=10
declare -rx PLAYBOOK_DIR="${HOME}/.ansible/playbooks"
declare -rx ANSIBLE_INVENTORY_PLUGINS="${ANSIBLE_HOME}/plugins/inventory"
declare -rx INVENTORY_HOME="${ANSIBLE_HOME}/inventory"
declare -rx ANSIBLE_INVENTORY="${INVENTORY_HOME}"
declare -rx INVENTORY_ENABLED="community.general.proxmox,community.general.nmap,microsoft.ad.ldap,community.docker.docker_containers,ini,toml,yaml,json"
declare -rx ANSIBLE_GATHERING="smart"
declare -rx CACHE_PLUGIN="redis"
declare -rx CACHE_PLUGIN_CONNECTION="localhost:6379:0"
declare -rx CACHE_PLUGIN_PREFIX="ansible_facts"
declare -rx CALLBACKS_ENABLED="yaml,json,community.general.yaml"
declare -rx COLLECTIONS_PATHS="~/.ansible/collections"
declare -rx ANSIBLE_CALLBACKS_ENABLED=true
declare -rx ANSIBLE_ROLES_PATH="~/.ansible/roles"
declare -rx ANSIBLE_PIPELINING=true
declare -rx ANSIBLE_HOST_KEY_CHECKING=false
declare -rx ANSIBLE_PRIVATE_KEY_FILE="${HOME}/.ssh/id_ed25519"

declare -r A_HOSTS="${INVENTORY_HOME}/hosts.yaml"
declare -r GLOBAL_VARS_DIR="${ANSIBLE_HOME}/global_vars"
declare -r HOST_VARS_DIR="${ANSIBLE_HOME}/host_vars"
declare -r GROUP_VARS_DIR="${ANSIBLE_HOME}/group_vars"
declare -r COLLECTION_RDB_URL=https://github.com/robertdebock/ansible-collection-roles/tree/master/roles

declare -r ABI_ROLE="ansible.builtin.import_role"
declare -r ABSetup="ansible.builtin.setup"
declare -r ABShell="ansible.builtin.shell"
declare -r ABCommand="ansible.builtin.command"
declare -r ABScript="ansible.builtin.script"
declare -r ABW_Connection="ansible.builtin.wait_for_connection"
declare -r ABA_Host="ansible.builtin.add_host"
declare -r ABT_YAML="ansible.builtin.to_yaml"
declare -r ABT_JSON="ansible.builtin.to_json"
declare -r ABG_URL="ansible.builtin.get_url"
declare -r ABL_IN_File="ansible.builtin.lineinfile"

declare -r SYS_PYTHON="{'ansible_python_interpreter': '/usr/bin/python3'}"

# [ansible env config variables](https://docs.ansible.com/ansible/latest/reference_appendices/config.html)
## home location for env params that don't exist or I'm too lazy to look up
declare -rx ANSIBLE_CONFIG=~/.ansible.cfg

function _remove_app_host_key() {
  # remove any eisting host key from known hosts
   ansible localhost -m ansible.builtin.known_hosts -a "name=${APP_NAME} state=absent"
   ansible localhost -m ansible.builtin.known_hosts -a "name=${APP_NAME}.${ALT_DOMAIN_NAME} state=absent"
}

function _dump_inventory() {
  INFO "Dumping dynamic inventory to ${ANSIBLE_INVENTORY}/hosts.yaml"
  ansible-inventory all --export --list --yaml --inventory "${ANSIBLE_INVENTORY}" --output "${A_HOSTS}" || exit 5
}

function _add_to_inventory() {
  local APP_NAME="${1}"

  # add container to localhost hosts file so that the new container can be "found" -- use ansible variables rather than shell
   ansible localhost -m "${ABA_Host}" -a 'hostname={{ pve_lxc_net_interfaces[0].ip4 }} ansible_ssh_host={{ pve_hostname }} ansible_ssh_port=22' -e @"${HOST_VARS_DIR}/${APP_NAME}.yaml" || exit 5

  # making the inventory aware is not sufficient, but dns will register the target after provisioning and updating is a PITA with adhoc
   ansible localhost -m "${ABL_IN_File}" -a 'dest=/etc/hosts regexp=.*{{ pve_lxc_net_interfaces[0].ip4 }} line="{{ pve_lxc_net_interfaces[0].ip4 }} {{ pve_hostname }}.{{ pve_lxc_searchdomain }} {{ pve_hostname }}" state=present' -e @"${ANSIBLE_INVENTORY}/host_vars/${APP_NAME}.yaml" -e "${SYS_PYTHON}" --become || exit 5
}

# Called each and every time to either create the lxc, or bring it up to date according to personal preferences -- always assume the container exists at this point
function _setup_or_upgrade_lxc() {
  local APP_NAME="${1}"

  if ! [[ -f "${HOST_VARS_DIR}/${APP_NAME}".yaml ]]; then
    init_lxc_cmd "${1}"
  else
    INFO "Host vars detected.  Installing ${APP_NAME}"
  fi

  # TODO: Force flag
  INFO "Validating roles and collections"
   ansible-galaxy collection install -r "${AROOT}/collections/requirements.yml"
   ansible-galaxy role install -r "${AROOT}/roles/requirements.yml"

  # Host does not exist at this point -- no facts that influence connection should be set.  Creation of an lxc/kvm always requires a proxmox control node
  INFO "Setting up ${APP_NAME} using values in ${HOST_VARS_DIR}/${APP_NAME}.yaml"
   ansible localhost -m "${ABI_ROLE}" -a name=technohouser.proxmox.create_lxc -e @"${HOST_VARS_DIR}/${APP_NAME}.yaml" -e @"${GLOBAL_VARS_DIR}/all.yaml" -e @"${GROUP_VARS_DIR}/proxmox_all_lxc.yaml" || exit 5

  _add_to_inventory "${APP_NAME}"

  # need to refresh inventory so that the cache is aware of the new container
  _dump_inventory

   ansible "${APP_NAME}" -m "${ABSetup}" --user root || exit 5

  # Switch target host to pyenv venv -- last container step to use system python
   ansible "${APP_NAME}" -m "${ABI_ROLE}" -a name="staticdev.pyenv" --user root || exit 5

  # bypass cache here by using the exported inventory as well as the global sources
   ansible "${APP_NAME}" -m "${ABI_ROLE}" -a name="robertdebock.roles.locale" -e @"${HOST_VARS_DIR}/${APP_NAME}.yaml" --user root || exit 5
   ansible "${APP_NAME}" -m "${ABI_ROLE}" -a name="technohouser.bootstrap-common" -e @"${HOST_VARS_DIR}/${APP_NAME}.yaml" --user root || exit 5
   ansible "${APP_NAME}" -m "${ABI_ROLE}" -a name="technohouser.ansible-svc-user" -e @"${HOST_VARS_DIR}/${APP_NAME}.yaml" --user ansible || exit 5
}

function _run_playbook() {
  local _playbook="${1}"

  _dump_inventory

   ansible-playbook "${_playbook}" -i "${A_HOSTS}" --user ansible --become
}

function init_lxc_cmd() {
  local APP_NAME="${1}"

  # TODO: check that required values have been populated
  # TODO: hostname verification
  if ! [[ -f "${HOST_VARS_DIR}/${APP_NAME}".yaml ]]; then
    ERROR "No hostvars exist for the lxc app you intend to setup.  Copying template to ${HOST_VARS_DIR}/${APP_NAME}.yaml"

    # copy the typical customizations for an lxc for the new hosts (primarily ip, vmid, and hostname)
    cp "${AROOT}/inventory/host_vars/sample-lxc.yml" "${HOST_VARS_DIR}/${APP_NAME}.yaml"

    yq -i '.pve_hostname = strenv(APP_NAME)' "${HOST_VARS_DIR}/${APP_NAME}.yaml" || exit 7

    exit 2
  fi
}

function init_role_cmd() {
  local _ROLE_NAME=$1
   ansible-galaxy role init "${AROOT}/roles/${_ROLE_NAME}"
}

# Create/delete/modify with containers should always be against the ansible control node as the target for the proxmox module is the api
function destroy_lxc_cmd() {
  local APP_NAME="${1}"
  _remove_app_host_key "${1}"
   ansible localhost -m "${ABI_ROLE}" -a name=technohouser.destroy_lxc -e @"${HOST_VARS_DIR}/${APP_NAME}.yaml" || exit 5
   ansible localhost -m "${ABL_IN_File}" -a 'dest=/etc/hosts regexp=.*{{ pve_lxc_net_interfaces[0].ip4 }} line="{{ pve_lxc_net_interfaces[0].ip4 }} {{ pve_hostname }}.{{ pve_lxc_searchdomain }} {{ pve_hostname }}" state=absent' -e @"${HOST_VARS_DIR}/${APP_NAME}.yaml" --become || exit 5
  _dump_inventory
}

function setup_generic_cmd() {
  local APP_NAME="${1}"
  INFO "Setting up ${APP_NAME}"
  _dump_inventory
  _remove_app_host_key "${1}"
  _setup_or_upgrade_lxc "${1}"
}
