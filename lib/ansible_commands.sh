#!/usr/bin/env bash
# ansible folder paths
declare -rx ANSIBLE_HOME="${HOME}/.ansible"
declare -rx ANSIBLE_FORKS=10
declare -rx PLAYBOOK_DIR="${HOME}/.ansible/playbooks"
declare -rx ANSIBLE_INVENTORY_PLUGINS="${ANSIBLE_HOME}/plugins/inventory"
declare -rx INVENTORY_HOME="${ANSIBLE_HOME}/inventory"
declare -rx ANSIBLE_INVENTORY="${INVENTORY_HOME}"
declare -rx INVENTORY_ENABLED="community.general.nmap,microsoft.ad.ldap,community.docker.docker_containers,ini,toml,yaml,json,community.general.proxmox"
declare -rx ANSIBLE_GATHERING="smart"
declare -rx ANSIBLE_CACHE_PLUGIN="redis"
declare -rx ANSIBLE_CACHE_PLUGIN_CONNECTION="localhost:6379:0"
declare -rx COLLECTIONS_PATHS="~/.ansible/collections:${PROOT}/ansible/roles"
declare -rx ANSIBLE_ROLES_PATH="~/.ansible/roles:${PROOT}/ansible/roles"
declare -rx ANSIBLE_PIPELINING=true
declare -rx ANSIBLE_HOST_KEY_CHECKING=false
declare -rx ANSIBLE_PRIVATE_KEY_FILE="${HOME}/.ssh/id_ed25519"
declare -rx ANSIBLE_INJECT_FACT_VARS=true

declare -rx ANSIBLE_LOAD_CALLBACK_PLUGINS=1
declare -rx ANSIBLE_CALLBACKS_ENABLED="json,yaml"
declare -rx ANSIBLE_DISPLAY_SKIPPED_HOSTS=false
declare -rx ANSIBLE_CALLBACK_RESULT_FORMAT="yaml"
declare -rx ANSIBLE_DISPLAY_FAILED_STDERR=true

declare -rx A_HOSTS="${INVENTORY_HOME}/hosts.yaml"
declare -rx GLOBAL_VARS_DIR="${ANSIBLE_HOME}/global_vars"
declare -rx HOST_VARS_DIR="${INVENTORY_HOME}/host_vars"
declare -rx GROUP_VARS_DIR="${INVENTORY_HOME}/group_vars"
declare -rx COLLECTION_RDB_URL=https://github.com/robertdebock/ansible-collection-roles/tree/master/roles

declare -rx ABI_ROLE="ansible.builtin.import_role"
declare -rx ABSetup="ansible.builtin.setup"
declare -rx ABShell="ansible.builtin.shell"
declare -rx ABCommand="ansible.builtin.command"
declare -rx ABScript="ansible.builtin.script"
declare -rx ABW_Connection="ansible.builtin.wait_for_connection"
declare -rx ABA_Host="ansible.builtin.add_host"
declare -rx ABT_YAML="ansible.builtin.to_yaml"
declare -rx ABT_JSON="ansible.builtin.to_json"
declare -rx ABG_URL="ansible.builtin.get_url"
declare -rx ABL_IN_File="ansible.builtin.lineinfile"

# [ansible env config variables](https://docs.ansible.com/ansible/latest/reference_appendices/config.html)
## home location for env params that don't exist or I'm too lazy to look up
# declare -rx ANSIBLE_CONFIG="${PROOT}/ansible.cfg"

function _remove_app_host_key() {
  # remove any eisting host key from known hosts
  ansible localhost -m ansible.builtin.known_hosts -a "name=${APP_NAME} state=absent"
  ansible localhost -m ansible.builtin.known_hosts -a "name=${APP_NAME}.${ALT_DOMAIN_NAME} state=absent"
}

function _dump_inventory() {
  INFO "Dumping dynamic inventory to ${ANSIBLE_INVENTORY}/hosts.yaml"
  # ansible all -m "${ABSetup}" -i "${A_HOSTS}" 2>/dev/null
  ansible-inventory all --export --list --yaml --inventory "${ANSIBLE_INVENTORY}" --output "${A_HOSTS}" || exit 5
}

function _add_to_inventory() {
  local APP_NAME="${1}"

  # add container to localhost hosts file so that the new container can be "found" -- use ansible variables rather than shell
  ansible localhost -m "${ABA_Host}" -a 'hostname={{ pve_lxc_net_interfaces[0].ip4 }} ansible_ssh_host={{ pve_hostname }} ansible_ssh_port=22' -e @"${HOST_VARS_DIR}/${APP_NAME}.yaml" || exit 5

  # making the inventory aware is not sufficient, but dns will register the target after provisioning and updating is a PITA with adhoc
  ansible localhost -m "${ABL_IN_File}" -a 'dest=/etc/hosts regexp=.*{{ pve_lxc_net_interfaces[0].ip4 }} line="{{ pve_lxc_net_interfaces[0].ip4 }} {{ pve_hostname }}.{{ pve_lxc_searchdomain }} {{ pve_hostname }}" state=present' -e @"${ANSIBLE_INVENTORY}/host_vars/${APP_NAME}.yaml" --become || exit 5
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
  ansible-galaxy collection install -r "${PROOT}/ansible/collections/requirements.yml"
  ansible-galaxy role install -r "${PROOT}/ansible/roles/requirements.yml"

  # Host does not exist at this point -- no facts that influence connection should be set.  Creation of an lxc/kvm always requires a proxmox control node
  INFO "Setting up ${APP_NAME} using values in ${HOST_VARS_DIR}/${APP_NAME}.yaml"
  ansible localhost -m "${ABI_ROLE}" -a name=technohouser.proxmox.create_lxc -e @"${HOST_VARS_DIR}/${APP_NAME}.yaml" -e @"${GLOBAL_VARS_DIR}/all.yaml" -e @"${GROUP_VARS_DIR}/proxmox_all_lxc.yaml" || exit 5

  # bypass cache here by using the exported inventory as well as the global sources
  ansible "${APP_NAME}" -m "${ABI_ROLE}" -a name="technohouser.bootstrap" -e @"${HOST_VARS_DIR}/${APP_NAME}.yaml" -e @"${GLOBAL_VARS_DIR}/all.yaml" --user root || exit 5
  ansible "${APP_NAME}" -m "${ABI_ROLE}" -a name="technohouser.ansible" -e @"${HOST_VARS_DIR}/${APP_NAME}.yaml" -e @"${GLOBAL_VARS_DIR}/all.yaml" --user ansible || exit 5
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
    cp "${PROOT}/ansible/inventory/host_vars/sample-lxc.yml" "${HOST_VARS_DIR}/${APP_NAME}.yaml"

    yq -i '.pve_hostname = strenv(APP_NAME)' "${HOST_VARS_DIR}/${APP_NAME}.yaml" || exit 7

    exit 2
  fi
}

function init_role_cmd() {
  local _ROLE_NAME=$1
  ansible-galaxy role init "${PROOT}/ansible/roles/${_ROLE_NAME}"
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
