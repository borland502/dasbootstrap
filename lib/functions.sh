#!/usr/bin/env bash

# prevent chick/egg problem on chezmoi apply
if [[ ${XDG_LIB_HOME+x} ]]; then
    declare -x XDG_LIB_HOME="${HOME}/.local/lib"
fi

# shellcheck disable=SC1090,SC1091
source "${XDG_LIB_HOME}/constants.sh"
# shellcheck disable=SC1090,SC1091
source "${XDG_LIB_HOME}/logger.sh"
# shellcheck disable=SC1090,SC1091
source "${XDG_LIB_HOME}/install_doctor_functions.sh"
# shellcheck disable=SC1090,SC1091
source "${XDG_LIB_HOME}/util_functions.sh"
# shellcheck disable=SC1090,SC1091
source "${XDG_LIB_HOME}/task_functions.sh"

## lib scripts provided by chezmoi, which may or may not be present
if [[ -f "${XDG_LIB_HOME}/fzf-git.sh" ]]; then
    # shellcheck disable=SC1090,SC1091
    source "${XDG_LIB_HOME}/fzf-git.sh"
fi
