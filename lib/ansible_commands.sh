#!/usr/bin/env bash
# ansible folder paths
declare -r A_INVENTORY=${AROOT}/inventory
declare -r A_HOSTS=${A_INVENTORY}/hosts.yaml
declare -r INVENTORY=/etc/ansible/inventory
declare -r GLOBAL_VARS_DIR=/etc/ansible/global_vars
declare -r COLLECTION_RDB_URL=https://github.com/robertdebock/ansible-collection-roles/tree/master/roles

declare -r ABI_ROLE="ansible.builtin.import_role"
declare -r ABSetup="ansible.builtin.setup"
declare -r ABSshell="ansible.builtin.shell"
declare -r ABA_Host="ansible.builtin.add_host"
declare -r ABT_YAML="ansible.builtin.to_yaml"
declare -r ABT_JSON="ansible.builtin.to_json"

# [ansible env config variables](https://docs.ansible.com/ansible/latest/reference_appendices/config.html)
## home location for env params that don't exist or I'm too lazy to look up
declare -rx ANSIBLE_CONFIG=~/.ansible.cfg

# Called each and every time to either create the lxc, or bring it up to date according to personal preferences -- always assume the container exists at this point
function _setup_or_upgrade_lxc(){
  # need to refresh inventory so that the cache is aware of the new container
  ansible-inventory all --export --list --yaml --inventory "${INVENTORY}" --output ${A_INVENTORY}/hosts.yaml || exit 5

  # remove any eisting host key from known hosts
  ansible localhost -m ansible.builtin.known_hosts -a "name=${APP_NAME} state=absent"

  # bypass cache here by using the exported inventory
  ansible "${APP_NAME}" -m "${ABSetup}" -i "${A_HOSTS}" -e @"${A_INVENTORY}/host_vars/${APP_NAME}.yaml" --user root || exit 5
  ansible "${APP_NAME}" -m "${ABI_ROLE}" -a name="technohouser.bootstrap-common"  -e @"${A_INVENTORY}/host_vars/${APP_NAME}.yaml" --user root || exit 5
  ansible "${APP_NAME}" -m "${ABI_ROLE}" -a name="technohouser.ansible-svc-user" -e @"${A_INVENTORY}/host_vars/${APP_NAME}.yaml" --user "$(whoami)" || exit 5
}

# assume passwordless sudo, shell vars available to the svc account, and global ansible variables
function adhoc_shell(){
  local _stmt=$2

  ansible "${APP_NAME}" -m ansible.builtin.shell -a "${_stmt}" -e @/etc/ansible/global_vars/all.yaml --user "$(whoami)"
}

function init_role_cmd(){
  local _ROLE_NAME=$1
  ansible-galaxy role init "${AROOT}/roles/${_ROLE_NAME}"
}

function init_lxc_cmd(){
    # TODO: check that required values have been populated
    if ! [[ -f ${A_INVENTORY}/host_vars/${APP_NAME}.yaml ]]; then
      ERROR "No hostvars exist for the lxc app you intend to install.  Copying template to ${A_INVENTORY}/host_vars/${APP_NAME}.yaml"

      # copy customized sensitive defaults to sensitive host defaults for app, replace any existing
      cat "${GLOBAL_VARS_DIR}/all.yaml" "${GLOBAL_VARS_DIR}/pve.yaml" "${GLOBAL_VARS_DIR}/pve_lxc.yaml" "${GLOBAL_VARS_DIR}/host.yaml" > ${A_INVENTORY}/host_vars/${APP_NAME}.yaml

      yq -i '.pve_hostname = strenv(APP_NAME)' "${A_INVENTORY}/host_vars/${APP_NAME}.yaml" || exit 7

      ERROR "Customize the template and run again" && exit 2
    else
      INFO "Host vars detected.  Installing ${APP_NAME}"
    fi
    
    ansible-galaxy collection install -r "${AROOT}/collections/requirements.yml"
    ansible-galaxy role install -r "${AROOT}/roles/requirements.yml"

    # Host does not exist at this point -- no facts that influence connection should be set.  Creation of an lxc/kvm always requires a proxmox control node
    ansible localhost -m "${ABI_ROLE}" -a name=technohouser.proxmox.create_lxc -e @"${A_INVENTORY}/host_vars/${APP_NAME}.yaml" || exit 5
    _setup_or_upgrade_lxc
}

# Create/delete/modify with containers should always be against the ansible control node as the target for the proxmox module is the api 
function destroy_lxc_cmd(){
  local APP_NAME="${1}"

  ansible localhost -m "${ABI_ROLE}" -a name=technohouser.destroy_lxc -e @"${A_INVENTORY}/host_vars/${APP_NAME}.yaml" || exit 5
}

function install_generic_cmd(){
  local APP_NAME="${1}"
  init_lxc_cmd
}

## Single shot application installs.  Presumes existing lxc/kvm image with the application name.  Defaults from role are defined in host vars yaml.  all vars is presumed to be passed
function install_artifactory_oss_cmd(){
  local APP_NAME=${1}
  install_generic_cmd ${1}
  ansible "${APP_NAME}" -m "${ABI_ROLE}" -a 'name=robertdebock.roles.artifactory' -e @"${A_INVENTORY}/host_vars/${APP_NAME}.yaml" --user $(whoami) --become
}
