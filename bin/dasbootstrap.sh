#!/usr/bin/env bash

# path to script root -- presumes execution from the root dir (either dasbootstrap or ./bin/dasbootstrap.sh)
declare -rx PROOT="${XDG_DATA_HOME}/dasbootstrap"
declare -rx AROOT="${PROOT}/ansible"
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
	cmd install -- "Subcommands of install are usually application level, either system or user focused"
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
parser_definition_install() {
	setup   REST help:usage abbr:true -- \
		"Usage: ${2##*/} install [options...] [arguments...]"
	msg -- '' './dbs install scmplayer' ''
	msg -- 'Options:'
	# FLAG init -- initialize the underlying image as well as install the application
	cmd artifactory -- "Install artifactory repository"
	cmd harbor -- "Install harbor container repository"
	cmd gitea -- "Install gitea scm repository"
	cmd technitium -- "Install technitium dns"
}

# shellcheck disable=SC1083
parser_definition_destroy() {
	setup   REST help:usage abbr:true -- \
		"Usage: ${2##*/} exec [options...] [arguments...]"
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
		install)
			if [ $# -gt 0 ]; then
				cmd=$1
				shift
				case $cmd in
					artifactory)
						install_artifactory_oss_cmd "$cmd" "$@"
						;;
					docker)
						install_generic_docker_cmd "$cmd" "$@"
						;;
					harbor)
						install_harbor_cmd "$cmd" "$@"
						;;
					gitea)
						INFO "Installing gitea"
						install_gitea_cmd "$cmd" "$@"
						;;
					technitium)
						INFO "Installing technitium"
						install_technitium_cmd "$cmd" "$@"
						;;
					*)
						# perform bootstrap and common prep to all containers
						install_generic_cmd "$cmd" "$@"
						;;
				esac
			fi		
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
