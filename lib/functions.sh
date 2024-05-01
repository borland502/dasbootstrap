#!/usr/bin/env bash

if ! [[ ${DBS_SCROOT+x} ]]; then
  # shellcheck disable=SC2155
  declare -rx DBS_SCROOT=$(cd -P -- "$(dirname -- "$0")" && printf '%s\n' "$(pwd -P)")
fi

# shellcheck disable=SC1090
source "${DBS_SCROOT}/lib/constants.sh"
# shellcheck disable=SC1090
source "${DBS_SCROOT}/lib/install_doctor_functions.sh"
# shellcheck disable=SC1090
source "${DBS_SCROOT}/lib/util_functions.sh"
