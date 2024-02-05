#!/usr/bin/env bash
# ansible folder paths
declare -r A_INVENTORY=${AROOT}/inventory
declare -r A_HOSTS=${A_INVENTORY}/hosts.yaml
declare -r INVENTORY=/etc/ansible/inventory
declare -r GLOBAL_VARS_DIR=/etc/ansible/global_vars
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

# [ansible env config variables](https://docs.ansible.com/ansible/latest/reference_appendices/config.html)
## home location for env params that don't exist or I'm too lazy to look up
declare -rx ANSIBLE_CONFIG=~/.ansible.cfg

function init_lxc_cmd(){
  local APP_NAME="${1}"

    # TODO: check that required values have been populated
    # TODO: hostname verification
    if ! [[ -f ${A_INVENTORY}/host_vars/${APP_NAME}.yaml ]]; then
      ERROR "No hostvars exist for the lxc app you intend to install.  Copying template to ${A_INVENTORY}/host_vars/${APP_NAME}.yaml"

      # copy customized sensitive defaults to sensitive host defaults for app, replace any existing
      cat "${GLOBAL_VARS_DIR}/all.yaml" "${GLOBAL_VARS_DIR}/pve.yaml" "${GLOBAL_VARS_DIR}/pve_lxc.yaml" > ${A_INVENTORY}/host_vars/${APP_NAME}.yaml

      yq -i '.pve_hostname = strenv(APP_NAME)' "${A_INVENTORY}/host_vars/${APP_NAME}.yaml" || exit 7

      exit 2
    fi
}

# Called each and every time to either create the lxc, or bring it up to date according to personal preferences -- always assume the container exists at this point
function _setup_or_upgrade_lxc(){
  local APP_NAME="${1}"

  if ! [[ -f ${A_INVENTORY}/host_vars/${APP_NAME}.yaml ]]; then
    init_lxc_cmd "${1}"
  else
    INFO "Host vars detected.  Installing ${APP_NAME}"
  fi

  # Host does not exist at this point -- no facts that influence connection should be set.  Creation of an lxc/kvm always requires a proxmox control node
  INFO "Setting up ${APP_NAME} using values in ${A_INVENTORY}/host_vars/${APP_NAME}.yaml"
  ansible localhost -m "${ABI_ROLE}" -a name=technohouser.proxmox.create_lxc -e @"${A_INVENTORY}/host_vars/${APP_NAME}.yaml" || exit 5

  ansible-galaxy collection install -r "${AROOT}/collections/requirements.yml"
  ansible-galaxy role install -r "${AROOT}/roles/requirements.yml"

  # Give time for the ole proxmox to spin up lxc before proceeding
  ansible "${APP_NAME}" -m "${ABW_Connection}" -a "connect_timeout=5 delay=10 sleep=5 timeout=120" -i "${A_HOSTS}" -e @"${A_INVENTORY}/host_vars/${APP_NAME}.yaml" --user root || exit 5

  # need to refresh inventory so that the cache is aware of the new container
  ansible-inventory all --export --list --yaml --inventory "${INVENTORY}" --output ${A_INVENTORY}/hosts.yaml || exit 5

  # remove any eisting host key from known hosts
  ansible localhost -m ansible.builtin.known_hosts -a "name=${APP_NAME} state=absent"

  # bypass cache here by using the exported inventory as well as the global sources
  ansible "${APP_NAME}" -m "${ABSetup}" -i "${A_HOSTS}" -i "${INVENTORY}" -e @"${A_INVENTORY}/host_vars/${APP_NAME}.yaml" --user root || exit 5
  ansible "${APP_NAME}" -m "${ABI_ROLE}" -a name="technohouser.bootstrap-common"  -e @"${A_INVENTORY}/host_vars/${APP_NAME}.yaml" --user root || exit 5
  ansible "${APP_NAME}" -m "${ABI_ROLE}" -a name="technohouser.ansible-svc-user" -e @"${A_INVENTORY}/host_vars/${APP_NAME}.yaml" --user ansible || exit 5
}

function _install_docker(){
  local _ROLE_NAME=$1

  ansible "${APP_NAME}" -m "${ABI_ROLE}" -a 'name=robertdebock.roles.epel' -e @"${A_INVENTORY}/host_vars/${APP_NAME}.yaml" --user ansible --become  
  ansible "${APP_NAME}" -m "${ABI_ROLE}" -a 'name=robertdebock.roles.docker_ce' -e @"${A_INVENTORY}/host_vars/${APP_NAME}.yaml" --user ansible --become  
  ansible "${APP_NAME}" -m "${ABI_ROLE}" -a 'name=robertdebock.roles.docker_compose' -e @"${A_INVENTORY}/host_vars/${APP_NAME}.yaml" --user ansible --become
}

# assume passwordless sudo, shell vars available to the svc account, and global ansible variables
function adhoc_shell(){
  local _stmt=$2

  ansible "${APP_NAME}" -m ansible.builtin.shell -a "${_stmt}" -e @/etc/ansible/global_vars/all.yaml --user ansible
}

function init_role_cmd(){
  local _ROLE_NAME=$1
  ansible-galaxy role init "${AROOT}/roles/${_ROLE_NAME}"
}

# function init_kvm_cmd(){
#   if ! [[ -f ${A_INVENTORY}/host_vars/${APP_NAME}.yaml ]]; then
#       ERROR "No hostvars exist for the lxc app you intend to install.  Copying template to ${A_INVENTORY}/host_vars/${APP_NAME}.yaml"

#       # copy customized sensitive defaults to sensitive host defaults for app, replace any existing
#       cat "${GLOBAL_VARS_DIR}/all.yaml" "${GLOBAL_VARS_DIR}/pve.yaml" "${GLOBAL_VARS_DIR}/pve_lxc.yaml" > ${A_INVENTORY}/host_vars/${APP_NAME}.yaml

#       yq -i '.pve_hostname = strenv(APP_NAME)' "${A_INVENTORY}/host_vars/${APP_NAME}.yaml" || exit 7

#       ERROR "Customize the template and run again" && exit 2
#     else
#       INFO "Host vars detected.  Installing ${APP_NAME}"
#     fi
    
#     ansible-galaxy collection install -r "${AROOT}/collections/requirements.yml"
#     ansible-galaxy role install -r "${AROOT}/roles/requirements.yml"

#     # Host does not exist at this point -- no facts that influence connection should be set.  Creation of an lxc/kvm always requires a proxmox control node
#     ansible localhost -m "${ABI_ROLE}" -a name=technohouser.proxmox.create_lxc -e @"${A_INVENTORY}/host_vars/${APP_NAME}.yaml" || exit 5
#     _setup_or_upgrade_lxc
#   }
# }

# Create/delete/modify with containers should always be against the ansible control node as the target for the proxmox module is the api 
function destroy_lxc_cmd(){
  local APP_NAME="${1}"

  ansible localhost -m "${ABI_ROLE}" -a name=technohouser.destroy_lxc -e @"${A_INVENTORY}/host_vars/${APP_NAME}.yaml" || exit 5
}

function install_generic_cmd(){
  local APP_NAME="${1}"
  _setup_or_upgrade_lxc "${1}"
}

## Single shot application installs.  Presumes existing lxc/kvm image with the application name.  Defaults from role are defined in host vars yaml.  all vars is presumed to be passed
function install_artifactory_oss_cmd(){
  local APP_NAME=${1}
  install_generic_cmd ${1}
  ansible "${APP_NAME}" -m "${ABI_ROLE}" -a 'name=robertdebock.roles.artifactory' -e @"${A_INVENTORY}/host_vars/${APP_NAME}.yaml" --user ansible --become
}

function install_cloudflare_cmd(){
  local APP_NAME=${1}
  install_generic_cmd ${1}


}

# function install_gitbackup_cmd(){

# }

function install_gitea_cmd(){
  local APP_NAME=${1}
  install_generic_cmd ${1}

  ansible "${APP_NAME}" -m "${ABI_ROLE}" -a 'name=robertdebock.roles.gitea' -e @"${A_INVENTORY}/host_vars/${APP_NAME}.yaml" --user ansible --become
}

function install_harbor_cmd(){
  local APP_NAME=${1}
  install_generic_cmd ${1}
  _install_docker "${1}"
  ansible "${APP_NAME}" -m "${ABI_ROLE}" -a 'name=robertdebock.roles.selinux' -e @"${A_INVENTORY}/host_vars/${APP_NAME}.yaml" --user ansible --become
  ansible "${APP_NAME}" -m "${ABI_ROLE}" -a 'name=robertdebock.roles.harbor' -e @"${A_INVENTORY}/host_vars/${APP_NAME}.yaml" --user ansible --become
}

function install_redis_cmd(){
  local APP_NAME=${1}
  install_generic_cmd ${1}

  ansible "${APP_NAME}" -m "${ABI_ROLE}" -a 'name=robertdebock.roles.epel' -e @"${A_INVENTORY}/host_vars/${APP_NAME}.yaml" --user ansible --become
  ansible "${APP_NAME}" -m "${ABI_ROLE}" -a 'name=robertdebock.roles.apt_autostart' -e @"${A_INVENTORY}/host_vars/${APP_NAME}.yaml" --user ansible --become
  ansible "${APP_NAME}" -m "${ABI_ROLE}" -a 'name=robertdebock.roles.sys_ctl' -e @"${A_INVENTORY}/host_vars/${APP_NAME}.yaml" --user ansible --become
}

function install_technitium_cmd(){
  local APP_NAME=${1}
  install_generic_cmd ${1}

  ansible localhost -m "${ABG_URL}" -a 'url=https://download.technitium.com/dns/install.sh dest=/tmp/technitium_install.sh mode="0700"'
  ansible "${APP_NAME}" -m "${ABScript}" -a '/tmp/technitium_install.sh creates=/opt/technitium/dns' --user ansible --become
}

function install_generic_docker_cmd(){
  local APP_NAME=${1}
  install_generic_cmd ${1}
  _install_docker ${1}
}