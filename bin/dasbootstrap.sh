#!/usr/bin/env bash

# path to script root -- presumes execution from the root dir (either dasbootstrap or ./bin/dasbootstrap.sh)
declare -r PROOT="$(pwd)"
declare -r AROOT="${PROOT}/ansible"
declare -r SCROOT="${PROOT}/bin"
declare -r LIBROOT="${PROOT}/lib"

# https://github.com/ko1nksm/getoptions
source "${LIBROOT}/getoptions.sh"
# https://github.com/jeliasson/zsh-logging
source "${LIBROOT}/logging.sh"
source "${LIBROOT}/ansible_commands.sh"
source "${LIBROOT}/shell_functions.sh"

# getoptions supports git style subcommands and these are the first level commands
parser_definition() {
	setup   REST help:usage abbr:true -- \
		"Usage: ${2##*/} [global options...] [command] [options...] [arguments...]"
	msg -- '' 'Dasbootstrap' ''
	msg -- 'Options:'
	param	INVENTORY	-i --inventory	-- "inventory"
	disp    :usage  -h --help
	disp    VERSION    --version

	msg -- '' 'Commands:'
	cmd init -- "Subcommands of init are not assured to be idepotent, but may be, as part of initializing a system"
	cmd install -- "Subcommands of install are usually application level, either system or user focused"
	cmd exec -- "Subcommands of exec are scripts or role-level actions vs Site or Playbook level as init"
	cmd test -- ""
	cmd destroy -- ""
	
}

# shellcheck disable=SC1083
parser_definition_init() {
	setup   REST help:usage abbr:true -- \
		"Usage: ${2##*/} init [options...] [arguments...]"
	msg -- '' 'getoptions init example' ''
	msg -- 'Options:'
	cmd ansible-controller -- "Initialize the ansible controller"
	cmd role -- "Initialize a new role within dasbootstrap"
	cmd lxc -- "Initialize / update a boostrap lxc"
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
	msg -- '' 'getoptions subcommand example' ''
	msg -- 'Options:'
}

# param   :'action "$1" p1 p2' --act1 --act2 var:param
# action() {
#	# Example of passing options and parameters
#	echo "Do action: option => [$1], param=>[$2, $3], arg => [$OPTARG]"
#	exit
# }

# ./dasbootstrap exec install_homebrew_pkg --act1 'hi' --act2 'bye' test
# Do action: option => [--act1], param=>[p1, p2], arg => [hi]
# Do action: option => [--act2], param=>[p1, p2], arg => [bye]

#

# shellcheck disable=SC1083
parser_definition_exec() {
	setup   REST help:usage abbr:true -- \
		"Usage: ${2##*/} exec [options...] [arguments...]"
	msg -- '' 'dasbootstrap exec adhoc -t "localhost" -m ansible.builtin.setup' ''
	msg -- '' 'dasbootstrap exec --mod setup' ''
	msg -- 'Options:'
	cmd adhoc -- "Execute an ansible adhoc action with a module"
	param :'shortcuts_cmd "$1" mod' --mod var:param
	disp    :usage  -h --help
}

# shellcheck disable=SC1083
parser_definition_destroy() {
	setup   REST help:usage abbr:true -- \
		"Usage: ${2##*/} exec [options...] [arguments...]"
	msg -- '' 'dasbootstrap exec --mod setup' ''
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
						destroy_lxc_cmd
						;;
					role)
						eval "$(getoptions parser_definition_init_role parse "$0")"
						parse "$@"
						eval "set -- $REST"

						init_role_cmd "$ROLE"
						;;
					lxc)
						init_lxc_cmd
						;;
					--)
				esac
			fi
			;;
		test)
			eval "$(getoptions parser_definition_install parse "$0")"
			parse "$@"
			eval "set -- $REST"
			echo "FLAG_B: $FLAG_B"
			;;
		exec)
			eval "$(getoptions parser_definition_exec parse "$0")"
			parse "$@"
			eval "set -- $REST"
			
			# if [ $# -gt 0 ]; then
			# 	cmd=$1
			# 	shift
			# 	case $cmd in
			# 		adhoc)
			# 			eval "$(getoptions parser_definition_ansible_cmds parse "$0")"
			# 			parse "$@"
			# 			eval "set -- $REST"

			# 			# ansible paramters available to the adhoc facade function
			# 			adhoc_action_cmd
			# 			;;
			# 		--)
			# 	esac
			# fi
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
						destroy_lxc_cmd
						;;
					--)
				esac
			fi
			;;	
		--) # no subcommand, arguments only
	esac
fi
