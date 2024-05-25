#!/usr/bin/env bash

# https://unix.stackexchange.com/questions/79064/how-to-export-variables-from-a-file
# use set +/- a for more portability (e.g. cygwin)
export_from() {
  # local is not a standard command but is pretty common. It's needed here
  # for this code to be re-entrant (for the case where sourced files to
  # call export_from). We still use _export_from_ prefix to namespace
  # those variables to reduce the risk of those variables being some of
  # those exported by the sourced file.
  local _export_from_ret _export_from_restore _export_from_file

  _export_from_ret=0

  # record current state of the allexport option. Some shells (ksh93/zsh)
  # have support for local scope for options, but there's no standard
  # equivalent.
  case "$-" in
    (*a*) _export_from_restore=;;
    (*)   _export_from_restore='set +a';;
  esac

  for _export_from_file do
    # using the command prefix removes the "special" attribute of the "."
    # command so that it doesn't exit the shell when failing.
    # shellcheck disable=SC1090
    source "$_export_from_file" || _export_from_ret="$?"
  done
  eval "$_export_from_restore"
  return "$_export_from_ret"
}

if [[ -f "${HOME}/.env" ]]; then
  export_from "${HOME}/.env"
fi

# has should always install first as it is used to check for subsequent installs
declare -ax BREW_LIST=(has gh age curl git rsync unison jq yq chezmoi java jenv vim starship tldr zsh zinit gcc gcc@11)
BREW_LIST+=(gum sshpass fzf direnv rg fd sd eza atuin prettyping nmap pyenv pipx poetry)
declare -ax PIPX_LIST=(poetry ansible ansible-lint)
