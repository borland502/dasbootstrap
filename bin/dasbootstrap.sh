#!/usr/bin/env bash

# dasbootstrap.sh assumes no previously installed elements and will attempt to use more common commands
# to retrieve them

# Fallback action in case the install is interrupted after root phase is done
if [[ $USER == "root" ]] && [[ -f '/root/.rootfinished' ]]; then
    # presume sudo powers at this point
    _username="$(cat /root/.rootfinished)"
    exec su - "${_username}" "/home/${_username}/$(basename "$0")"
fi

# @description Helper function for ensurePackageInstalled for Debian installations
function ensureDebianPackageInstalled() {
    if type sudo &> /dev/null && [ "$CAN_USE_SUDO" != 'false' ]; then
        sudo apt-get update
        sudo apt-get install -y "$1"
    else
        apt-get update
        apt-get install -y "$1"
    fi
}

# @description Ensures given package is installed on a system.
#
# @arg $1 string The name of the package that must be present
#
# @exitcode 0 The package(s) were successfully installed
# @exitcode 1+ If there was an error, the package needs to be installed manually, or if the OS is unsupported
function ensurePackageInstalled() {
    export CAN_USE_SUDO='true'
    # TODO: Restore other types later
    if ! [[ $(command -v "$1" ) ]]; then
        ensureDebianPackageInstalled "$1"
    fi
}

# @description If the user is running this script as root, then create a new user
# and restart the script with that user. This is required because Homebrew
# can only be invoked by non-root users.
function create_sudo_user(){
    local _username=${1:-'ansible'}

    ensurePackageInstalled "sudo"
    ensurePackageInstalled "zsh"

    if [ -z "$NO_INSTALL_HOMEBREW" ] && [ "$USER" == "root" ] && [ -z "$INIT_CWD" ] && type useradd &> /dev/null; then
        # shellcheck disable=SC2016
        logger info "Running as root - creating separate user named ${_username} to run script with"
        echo "${_username} ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
        useradd --create-home --shell "$(which zsh)" "${_username}" > /dev/null || ROOT_EXIT_CODE=$?
        if [ -n "$ROOT_EXIT_CODE" ]; then
            # shellcheck disable=SC2016
            logger info "User ${_username} already exists"
        fi

        cp "$0" "/home/${_username}/$(basename "$0")"
        chown "${_username}:${_username}" "/home/${_username}/$(basename "$0")"

        # use gum before chezmoi engages to ask for the age key
#        mkdir -p "/home/${_username}/.config/trapper_keeper"
        gum input --placeholder "Enter the age private key: " | tr -d '\n' >\
        "/home/${_username}/.config/trapper_keeper/key.txt"

#        mkdir -p "/home/${_username}/.local/state/trapper_keeper"
#        gum input --placeholder "Enter the keepassxc password: " | tr -d '\n' >\
#        "/home/${_username}/.local/state/trapper_keeper/keepass_token"

        chown -R "${_username}:${_username}" "/home/${_username}"

        # shellcheck disable=SC2016
        logger info "Reloading the script with the ${_username} user"
        echo "${_username}" > /root/.rootfinished
        exec su - "${_username}" "/home/${_username}/$(basename "$0")"
    fi
}

ensurePackageInstalled build-essential
ensurePackageInstalled "linux-headers-$(uname -r)"
ensurePackageInstalled git
ensurePackageInstalled curl
ensurePackageInstalled rsync
ensurePackageInstalled unison
ensurePackageInstalled gh
ensurePackageInstalled python3-full
ensurePackageInstalled pipx

if [[ $USER == "root" ]]; then
    # Choose the user that will be in control
    _user=$(gum choose {"ansible","$(whoami)"})

    curl -L https://github.com/charmbracelet/gum/releases/download/v0.14.0/gum_0.14.0_amd64.deb \
    -o gum.deb
    sudo dpkg -i gum.deb

    # Create a quick and dirty service user then restart the script as that user
    create_sudo_user "${_user}"
fi

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
# DBS_WORKING_DIR="${XDG_DATA_HOME}/dasbootstrap"
# shellcheck disable=SC2034
HOMEBREW_NO_INSTALL_CLEANUP=true
# shellcheck disable=SC2034
HOMEBREW_NO_ANALYTICS=1
CAN_USE_SUDO=1
# shellcheck disable=SC2034
HAS_ALLOW_UNSAFE=y

# Program versions
PYTHON=3.12
set +o allexport

mkdir -p "${XDG_CONFIG_HOME}"
mkdir -p "${XDG_CACHE_HOME}"
mkdir -p "${XDG_DATA_HOME}"
mkdir -p "${XDG_STATE_HOME}"
mkdir -p "${XDG_BIN_HOME}"
mkdir -p "${XDG_LIB_HOME}"

# Clone this project if the script is invoked alone
if ! [[ -d ${DBS_SCROOT} ]]; then
    git clone --single-branch --branch=main https://github.com/borland502/dasbootstrap.git "${DBS_SCROOT}"
else
    git pull --autostash --force "${DBS_SCROOT}"
fi

# Temporarily patch pyenv into path -- chezmoi will take care of the permanent job

curl https://pyenv.run | bash
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

#[[ "$(python --version 2>/dev/null)" == *"${PYTHON}"* ]] || sudo pyenv install "${PYTHON}"

# TODO: Copy over command files
find "${DBS_SCROOT}/bin" -name '*.sh' -exec cp {} "${XDG_BIN_HOME}/" \;
chown +x "${XDG_BIN_HOME}/*.sh"

find "${DBS_SCROOT}/lib" -name '*.sh' -exec cp {} "${XDG_LIB_HOME}/" \;

# Ensure changes between working directory and mirror are sync'd
# unison -batch=true -ignore 'Path {.git,.venv,.task,.cache,.vscode,dist}' "${DBS_WORKING_DIR}/" "${DBS_SCROOT}/"

# remove all the script links in bin / lib and establish them as hard links from the working directory
# cp -Ral "${DBS_SCROOT}/bin/" "${XDG_BIN_HOME}/"
# cp -Ral "${DBS_SCROOT}/lib/" "${XDG_LIB_HOME}/"

# rsync -avzPh "${DBS_SCROOT}/ansible/" "${ANSIBLE_HOME}/"

source "${XDG_LIB_HOME}/functions.sh"

bootstrap_ansible_node "${_user}"

for program in "${BREW_LIST[@]}"; do
    if ! [[ $(command -v "${program}") ]]; then
        brew install "${program}"
    fi
done

for program in "${PIPX_LIST[@]}"; do
    if ! [[ $(command -v "${program}") ]]; then
        pipx install "${program}"
    fi
done

if ! [[ -d "${XDG_DATA_HOME}/chezmoi" ]]; then
    git clone --single-branch --branch=main https://github.com/borland502/dotfiles.git "${XDG_DATA_HOME}/chezmoi"
else
    git pull --autostash --force "${XDG_DATA_HOME}/chezmoi"
fi

pyenv global "${PYTHON}"
cd "${DBS_SCROOT}" || (echo "Could not cd into ${DBS_SCROOT}"; exit 2)
poetry install

cd "${XDG_DATA_HOME}/chezmoi" || (echo "Could not cd into ${XDG_DATA_HOME}/chezmoi"; exit 2)
poetry install

chezmoi init
chezmoi apply
