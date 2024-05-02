#!/usr/bin/env bash

if ! [[ ${DBS_SCROOT+x} ]]; then
  # shellcheck disable=SC2155
  declare -rx DBS_SCROOT=${HOME}/.local/share/automation/dasbootstrap
fi
declare -rx HOMEBREW_NO_INSTALL_CLEANUP=true
declare -rx HOMEBREW_NO_ANALYTICS=1
declare -x CAN_USE_SUDO=1
