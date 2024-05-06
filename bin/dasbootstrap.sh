#!/usr/bin/env bash

# Essential constants -- though two of them are not actually in the XDG Spec
# shellcheck disable=SC2155
XDG_BIN_HOME="${HOME}/.local/bin"
XDG_LIB_HOME="${HOME}/.local/lib"
XDG_DATA_HOME="${HOME}/.local/share"

declare -rx XDG_BIN_HOME
declare -rx XDG_LIB_HOME
declare -rx XDG_DATA_HOME

# shellcheck disable=SC2155
declare -rx DBS_SCROOT="${XDG_DATA_HOME}/automation/dasbootstrap"
declare -rx DBS_WORKING_DIR="${XDG_DATA_HOME}/dasbootstrap"

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

# TODO: Create XDG spec dirs if they don't exist
mkdir -p "${HOME}"/.local/{"bin","lib","share/automation","state"}

if ! [[ -d ${DBS_SCROOT} ]]; then
    git clone --single-branch --branch=main https://github.com/borland502/dasbootstrap.git "${DBS_SCROOT}"
    # TODO: Update automation repos
else
    git pull --autostash --force "${DBS_SCROOT}"
fi

# Ensure changes between working directory and mirror are sync'd
unison -batch=true -ignore 'Path {.git,.venv}' "${DBS_WORKING_DIR}/" "${DBS_SCROOT}/"

# Copy all bin and lib files to their system homes
rsync -avzPh "${DBS_SCROOT}/bin/" "${XDG_BIN_HOME}/"
rsync -avzPh "${DBS_SCROOT}/lib/" "${XDG_LIB_HOME}/"

source "${XDG_LIB_HOME}/functions.sh"

bootstrap_ansible_node
installTask
