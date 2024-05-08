#!/usr/bin/env bash

# dasbootstrap.sh assumes no previously installed elements and will attempt to use more common commands
# to retrieve them

mkdir -p "${HOME}"/.local/{"bin","lib","share/automation","state","config"}

# Essential constants
# XDG Spec
set -o allexport
XDG_CONFIG_HOME="${HOME}/.config"
# shellcheck disable=SC2034
XDG_CACHE_HOME="${HOME}/.cache"
XDG_DATA_HOME="${HOME}/.local/share"
# shellcheck disable=SC2034
XDG_STATE_HOME="${HOME}/.local/state"
# shellcheck disable=SC2034
XDG_DATA_DIRS="/usr/local/share:/usr/share:${XDG_DATA_HOME}/var/lib/flatpak/exports/share:${XDG_DATA_HOME}/flatpak/exports/share"
# shellcheck disable=SC2034
XDG_CONFIG_DIRS="/etc/xdg:${XDG_CONFIG_HOME}"
# XDG Spec adjacent
XDG_BIN_HOME="${HOME}/.local/bin"
XDG_LIB_HOME="${HOME}/.local/lib"

ANSIBLE_HOME="${HOME}/.ansible"

DBS_SCROOT="${XDG_DATA_HOME}/automation/dasbootstrap"
DBS_WORKING_DIR="${HOME}/.local/share/dasbootstrap"
# shellcheck disable=SC2034
HOMEBREW_NO_INSTALL_CLEANUP=true
# shellcheck disable=SC2034
HOMEBREW_NO_ANALYTICS=1
CAN_USE_SUDO=1
# shellcheck disable=SC2034
HAS_ALLOW_UNSAFE=y

# Program versions
PYTHON=3.11
set +o allexport

# @description Ensures given package is installed on a system.
#
# @arg $1 string The name of the package that must be present
#
# @exitcode 0 The package(s) were successfully installed
# @exitcode 1+ If there was an error, the package needs to be installed manually, or if the OS is unsupported
function ensurePackageInstalled() {
    export CAN_USE_SUDO='true'
    if ! type "$1" &> /dev/null; then
        if [[ "$OSTYPE" == 'darwin'* ]]; then
            brew install "$1"
            elif [[ "$OSTYPE" == 'linux'* ]]; then
            if [ -f "/etc/redhat-release" ]; then
                ensureRedHatPackageInstalled "$1"
                elif [ -f "/etc/debian_version" ]; then
                ensureDebianPackageInstalled "$1"
                elif [ -f "/etc/arch-release" ]; then
                ensureArchPackageInstalled "$1"
                elif [ -f "/etc/alpine-release" ]; then
                ensureAlpinePackageInstalled "$1"
                elif type dnf &> /dev/null || type yum &> /dev/null; then
                ensureRedHatPackageInstalled "$1"
                elif type apt-get &> /dev/null; then
                ensureDebianPackageInstalled "$1"
                elif type pacman &> /dev/null; then
                ensureArchPackageInstalled "$1"
                elif type apk &> /dev/null; then
                ensureAlpinePackageInstalled "$1"
            else
                logger error "$1 is missing. Please install $1 to continue." && exit 1
            fi
            elif [[ "$OSTYPE" == 'cygwin' ]] || [[ "$OSTYPE" == 'msys' ]] || [[ "$OSTYPE" == 'win32' ]]; then
            logger error "Windows is not directly supported. Use WSL or Docker." && exit 1
            elif [[ "$OSTYPE" == 'freebsd'* ]]; then
            logger error "FreeBSD support not added yet" && exit 1
        else
            logger error "System type not recognized"
        fi
    fi
}

ensurePackageInstalled git
ensurePackageInstalled curl
ensurePackageInstalled rsync
ensurePackageInstalled unison
ensurePackageInstalled gh

if ! [[ -d ${DBS_SCROOT} ]]; then
    git clone --single-branch --branch=main https://github.com/borland502/dasbootstrap.git "${DBS_SCROOT}"
else
    git pull --autostash --force "${DBS_SCROOT}"
fi

# Ensure changes between working directory and mirror are sync'd
unison -batch=true -ignore 'Path {.git,.venv,.task,.cache,.vscode,dist}' "${DBS_WORKING_DIR}/" "${DBS_SCROOT}/"

# Copy all bin and lib files to their system homes
rsync -avzPh "${DBS_SCROOT}/bin/" "${XDG_BIN_HOME}/"
rsync -avzPh "${DBS_SCROOT}/lib/" "${XDG_LIB_HOME}/"
rsync -avzPh "${DBS_SCROOT}/ansible/" "${ANSIBLE_HOME}/"

source "${XDG_LIB_HOME}/functions.sh"

bootstrap_ansible_node
installTask

for program in "${BREW_LIST[@]}"; do
  if ! has "${program}"; then
    brew install "${program}"
  fi
done

pyenv install "${PYTHON}"

for program in "${PIPX_LIST[@]}"; do
  if ! has "${program}"; then
    pipx install "${program}"
  fi
done

