#!/usr/bin/env bash

###
# More truthy than strictly constants
###

if ! [[ ${DBS_SCROOT+x} ]]; then
  # shellcheck disable=SC2155
  declare -rx DBS_SCROOT=${HOME}/.local/share/automation/dasbootstrap
  declare -rx LROOT=$HOME/.local/lib
  declare -rx SCROOT=${XDG_DATA_BIN:-${HOME}/.local/lib}
fi

declare -rx HOMEBREW_NO_INSTALL_CLEANUP=true
declare -rx HOMEBREW_NO_ANALYTICS=1
declare -x CAN_USE_SUDO=1
