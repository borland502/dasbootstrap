#!/usr/bin/env bash

# facade for the ansible command
# parser_definition_ansible_cmds() {
# 	setup   REST help:usage abbr:true -- \
# 		"Usage: ${2##*/} cmd2 [options...] [arguments...]"
# 	msg -- '' 'getoptions subcommand example' ''
# 	msg -- 'Options:'
#   param   ARGS        -a --args         -- 'specify command or module arguments'
#   param   TARGET      -t --target       -- 'host or group out of inventory to act on'
#   param   INVENTORY   -i --inventory    -- 'specify inventory host file or host list'  
#   param   MODULE      -m --module-name  -- 'specify action to execute'
# 	disp    :usage  -h --help
# }

# function adhoc_action_cmd() {
#   ansible "$TARGET" -m "$MODULE" -a "$ARGS" -i "$INVENTORY"
# }

# common adhoc ansible commands that assume defaults like inventory paths are set
function shortcuts_cmd(){
  case $OPTARG in
    setup)
      ansible all -m ansible.builtin.setup
      ;;
    destroy)
      ;;
    --)
  esac
}

function init_role_cmd(){
  local _ROLE_NAME=$1
  ansible-galaxy role init "${AROOT}/roles/${_ROLE_NAME}"
}

function init_lxc_cmd(){
  ansible-playbook "${AROOT}/playbooks/debian_lxc_bootstrap.yaml" -i /etc/ansible/inventory/proxmox_bootstrap.yaml
}

function destroy_lxc_cmd(){
  ansible localhost -m ansible.builtin.import_role -a name=technohouser.destroy_lxc -e @/etc/ansible/global_vars/pve_lxc.yaml -e @/etc/ansible/global_vars/pve.yaml
}