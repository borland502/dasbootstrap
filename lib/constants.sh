#!/usr/bin/env bash

###
# More truthy than strictly constants
###

# Presume this is loaded
if ! [[ ${DBS_SCROOT+x} ]]; then
    # shellcheck disable=SC2155
    declare -rx DBS_SCROOT=${XDG_DATA_HOME}/automation/dasbootstrap
    declare -rx DBS_WORKING_DIR="${HOME}/.local/share/dasbootstrap"
fi
declare -rx HOMEBREW_NO_INSTALL_CLEANUP=true
declare -rx HOMEBREW_NO_ANALYTICS=1
declare -x CAN_USE_SUDO=1
