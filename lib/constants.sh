#!/usr/bin/env bash

if ! [[ ${DBS_SCROOT+x} ]]; then
  # shellcheck disable=SC2155
  declare -rx DBS_SCROOT=$(dirname "$(cd -P -- "$(dirname -- "$0")" && printf '%s\n' "$(pwd -P)")")
fi
declare -rx HOMEBREW_NO_INSTALL_CLEANUP=true
declare -rx HOMEBREW_NO_ANALYTICS=1
declare -x CAN_USE_SUDO=1
