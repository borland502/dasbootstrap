#!/usr/bin/env bash

# path to script root -- presumes execution from the root dir (either dasbootstrap or ./bin/dasbootstrap.sh)
declare -rx PROOT="${XDG_DATA_HOME}/dasbootstrap"
declare -rx AROOT="${PROOT}/ansible"
declare -rx PLAY_ROOT="${AROOT}/playbooks"
declare -rx SCROOT="${PROOT}/bin"
declare -rx LIBROOT="${PROOT}/lib"

# https://github.com/ko1nksm/getoptions
source "${LIBROOT}/getoptions.sh"
# https://github.com/jeliasson/zsh-logging
source "${LIBROOT}/logging.sh"
source "${LIBROOT}/ansible_commands.sh"
source "${LIBROOT}/shell_functions.sh"

# getoptions supports git style subcommands and these are the first level commands
parser_definition() {
	setup   REST plus:true help:usage abbr:true -- \
		"Usage: ${2##*/} [global options...] [command] [options...] [arguments...]"
	msg -- '' 'Dasbootstrap' ''
	msg -- 'Options:'
	param NODE -n --node init:="noctis" -- "Target Proxmox Node"
	disp    :usage  -h --help
	disp    VERSION    --version
	# msg -- '' 'Flags:'
	# FLAG DEBUG +d on:1 init:@unset
	msg -- '' 'Commands:'
	cmd init -- "Subcommands of init are not assured to be idepotent, but may be, as part of initializing a system"
	cmd setup -- "Subcommands of setup are usually application level, either system or user focused"
	cmd update -- "Update one or more containers with the assumption that those containers exist"
	cmd destroy -- ""
	# param :'shortcuts_cmd "$1" mod' --mod var:param
}

# shellcheck disable=SC1083
parser_definition_init() {
	setup   REST help:usage abbr:true -- \
		"Usage: ${2##*/} init [options...] [arguments...]"
	msg -- '' 'getoptions init example' ''
	msg -- 'Options:'
	cmd ansible-controller -- "Initialize the ansible controller"
	cmd role -- "Initialize a new role within dasbootstrap"
	cmd lxc -- "Initialize lxc hostvars template"
	disp    :usage  -h --help
}

parser_definition_init_role() {
	setup   REST help:usage abbr:true -- \
		"Usage: ${2##*/} role [options...] [arguments...]"
	msg -- '' 'getoptions init example' ''
	msg -- 'Options:'
	param ROLE -r --role -- "Role to initialize"
	disp    :usage  -h --help
}

# shellcheck disable=SC1083
parser_definition_setup() {
	setup   REST help:usage abbr:true -- \
		"Usage: ${2##*/} setup [options...] [arguments...]"
	msg -- '' './dbs setup scmplayer' ''
	msg -- 'Options:'
	# FLAG M_TEST -t --molecule-test -- "Use moledule to test installation"
	cmd harbor -- "setup harbor container repository"
	cmd gitea -- "setup gitea scm repository"
	cmd cronicle -- "setup cronicle cron manager"
}

# shellcheck disable=SC1083
parser_definition_destroy() {
	setup   REST help:usage abbr:true -- \
		"Usage: ${2##*/} destroy [options...] [arguments...]"
	msg -- '' './dbs destroy lxc scmplayer' ''
	msg -- 'Options:'
	cmd lxc -- "Destroy the bootstrap lxc container"
	cmd kvm -- "Destroy the bootstrap kvm"
	disp    :usage  -h --help
}

eval "$(getoptions parser_definition parse "$0") exit 1"
parse "$@"
eval "set -- $REST"

if [ $# -gt 0 ]; then
	cmd=$1
	shift
	case $cmd in
		init)
			eval "$(getoptions parser_definition_init parse "$0")"
			parse "$@"
			eval "set -- $REST"

			if [ $# -gt 0 ]; then
				cmd=$1
				shift
				case $cmd in
					ansible-controller)
						ERROR "Not implemented yet"
						;;
					role)
						eval "$(getoptions parser_definition_init_role parse "$0")"
						parse "$@"
						eval "set -- $REST"

						init_role_cmd "$ROLE"
						;;
					lxc)
						init_lxc_cmd "$1"
						;;
					--)
				esac
			fi
			;;
		setup)
			if [ $# -gt 0 ]; then
				cmd=$1
				shift
				case $cmd in
					docker)
						INFO "Setting up docker"
						setup_generic_cmd "$cmd" "$@"
						_run_playbook ansible/playbooks/applications/docker.yaml
						;;
					harbor)
						INFO "Setting up harbor"
						setup_generic_cmd "$cmd" "$@"
						_run_playbook ansible/playbooks/applications/harbor.yaml
						;;
					gitea)
						INFO "Setting up gitea"
						setup_generic_cmd "$cmd" "$@"
						_run_playbook ansible/playbooks/applications/gitea.yaml
						;;
					technitiumdns)
						INFO "Setting up Technitium DNS"
						setup_generic_cmd "$cmd" "$@"
						_run_playbook ansible/playbooks/applications/technitium.yaml
						;;
					*)
						# perform bootstrap and common prep to all containers
						setup_generic_cmd "$cmd" "$@"
						;;
				esac
			fi		
			;;
		update)
				# TODO: add flags and params for 1..N lxc, 1..N qemu
				_run_playbook ansible/playbooks/maintenance/update_running_lxcs.yaml 
			;;
		destroy)
			eval "$(getoptions parser_definition_destroy parse "$0")"
			parse "$@"
			eval "set -- $REST"

			if [ $# -gt 0 ]; then
				cmd=$1
				shift
				case $cmd in
					lxc)
						destroy_lxc_cmd "$@"
						;;
					--)
				esac
			fi
			;;	
		--) # no subcommand, arguments only
	esac
fi
