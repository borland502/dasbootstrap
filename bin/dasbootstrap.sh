#!/usr/bin/env bash

# https://unix.stackexchange.com/questions/76505/unix-portable-way-to-get-scripts-absolute-path-in-zsh
# zsh specific way to do (readlink -f) where a symbolic link in ~/.local/bin or the symbolic link in ~/.local/share/dasbootstrap/ both resolve to ~/.local/share/dasbootstrap
# declare -rx DBS_SCROOT=${0:A:h:h}
# A portable way to do the same from the post
# source "$(cd -P -- "$(dirname -- "$0")" && printf '%s\n' "$(pwd -P)")/lib/functions.sh"

# TODO: Flag rather than positional
# bootstrap_ansible_node 'ansible'

# TODO: Refactor as init script
# poetry run python -m "pyprojects.dasbootstrap.src.dasbootstrap" "$@"
