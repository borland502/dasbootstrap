#!/usr/bin/env bash


function ensure_permissions(){
    if [ -n "$CI" ]; then
        if type sudo &> /dev/null; then
            sudo chown -R "$(whoami):$(whoami)" .
        fi
    fi
}

# @description Ensure "${XDG_DATA_HOME}/lib/logger.sh" is present
function ensure_logdir(){
    if [ ! -f "${XDG_LIB_HOME}/logger.sh" ]; then
        mkdir -p .config
        if type curl &> /dev/null; then
            curl -sSL https://gitlab.com/megabyte-labs/common/shared/-/raw/master/common/lib/log > "${XDG_LIB_HOME}/logger.sh"
        fi
    fi

    chmod +x "${XDG_LIB_HOME}/logger.sh"
}


# @description Acquire unique ID for this script
function set_script_id(){
    if [ -z "$CI" ]; then
        if type md5sum &> /dev/null; then
            FILE_HASH="$(md5sum "$0" | sed 's/\s.*$//')"
        else
            FILE_HASH="$(date -r "$0" +%s)"
        fi
    else
        FILE_HASH="none"
    fi
}

# @description Caches values from commands
function cache() {
    local DIR="${CACHE_DIR:-.cache}"
    if ! test -d "$DIR"; then
        mkdir -p "$DIR"
    fi
    local FN="$DIR/${LINENO}-${FILE_HASH}"
    if ! test -f "$FN" ; then
        "$@" > "$FN"
    fi
    cat "$FN"
}

# @description Formats log statements
function format() {
    # shellcheck disable=SC2001,SC2016
    ANSI_STR="$(echo "$1" | sed 's/^\([^`]*\)`\([^`]*\)`/\1\\e[100;1m \2 \\e[0;39m/')"
    if [[ $ANSI_STR == *'`'*'`'* ]]; then
        ANSI_STR="$(format "$ANSI_STR")"
    fi
    echo -e "$ANSI_STR"
}

# @description Proxy function for handling logs in this script
function logger() {
    if [ -f "${XDG_LIB_HOME}/logger.sh" ]; then
        "${XDG_LIB_HOME}/logger.sh" "$1" "$2"
    else
        if [ "$1" == 'error' ]; then
            echo -e "\e[1;41m  ERROR   \e[0m $(format "$2")\e[0;39m"
            elif [ "$1" == 'info' ]; then
            echo -e "\e[1;46m   INFO   \e[0m $(format "$2")\e[0;39m"
            elif [ "$1" == 'success' ]; then
            echo -e "\e[1;42m SUCCESS  \e[0m $(format "$2")\e[0;39m"
            elif [ "$1" == 'warn' ]; then
            echo -e "\e[1;43m WARNING  \e[0m $(format "$2")\e[0;39m"
        else
            echo "$2"
        fi
    fi
}

# @description Helper function for ensurePackageInstalled for Alpine installations
function ensureAlpinePackageInstalled() {
    if type sudo &> /dev/null && [ "$CAN_USE_SUDO" != 'false' ]; then
        sudo apk --no-cache add "$1"
    else
        apk --no-cache add "$1"
    fi
}

# @description Helper function for ensurePackageInstalled for ArchLinux installations
function ensureArchPackageInstalled() {
    if type sudo &> /dev/null && [ "$CAN_USE_SUDO" != 'false' ]; then
        sudo pacman update
        sudo pacman -S "$1"
    else
        pacman update
        pacman -S "$1"
    fi
}

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

# @description Helper function for ensurePackageInstalled for RedHat installations
function ensureRedHatPackageInstalled() {
    if type sudo &> /dev/null && [ "$CAN_USE_SUDO" != 'false' ]; then
        if type dnf &> /dev/null; then
            sudo dnf install -y "$1"
        else
            sudo yum install -y "$1"
        fi
    else
        if type dnf &> /dev/null; then
            dnf install -y "$1"
        else
            yum install -y "$1"
        fi
    fi
}

# @description Installs package when user is root on Linux
#
# @arg $1 string The name of the package that must be present
#
# @exitcode 0 The package was successfully installed
# @exitcode 1+ If there was an error, the package needs to be installed manually, or if the OS is unsupported
function ensureRootPackageInstalled() {
    export CAN_USE_SUDO='false'
    if ! type "$1" &> /dev/null; then
        if [[ "$OSTYPE" == 'linux'* ]]; then
            if [ -f "/etc/redhat-release" ]; then
                ensureRedHatPackageInstalled "$1"
                elif [ -f "/etc/debian_version" ]; then
                ensureDebianPackageInstalled "$1"
                elif [ -f "/etc/arch-release" ]; then
                ensureArchPackageInstalled "$1"
                elif [ -f "/etc/alpine-release" ]; then
                ensureAlpinePackageInstalled "$1"
            fi
        fi
    fi
}

# @description If the user is running this script as root, then create a new user
# and restart the script with that user. This is required because Homebrew
# can only be invoked by non-root users.
function create_sudo_user(){
    local _username=${1:-'ansible'}

    ensureRootPackageInstalled "sudo"
    ensureRootPackageInstalled "zsh"

    if [ -z "$NO_INSTALL_HOMEBREW" ] && [ "$USER" == "root" ] && [ -z "$INIT_CWD" ] && type useradd &> /dev/null; then
        # shellcheck disable=SC2016
        logger info "Running as root - creating separate user named ${_username} to run script with"
        echo "${_username} ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
        useradd --create_home --shell "$(which zsh)" --gecos "" "${_username}" > /dev/null || ROOT_EXIT_CODE=$?
        if [ -n "$ROOT_EXIT_CODE" ]; then
            # shellcheck disable=SC2016
            logger info "User ${_username} already exists"
        fi

        # shellcheck disable=SC2016
        logger info "Reloading the script with the ${_username} user"
        exec su "${_username}" "$0" -- "$@"
    fi
}

# @description Ensures ~/.local/bin is in the PATH variable on *nix machines and
# exits with an error on unsupported OS types
#
# @set PATH string The updated PATH with a reference to ~/.local/bin
#
# @noarg
#
# @exitcode 0 If the PATH was appropriately updated or did not need updating
# @exitcode 1+ If the OS is unsupported
function ensureLocalPath() {
    if [[ "$OSTYPE" == 'darwin'* ]] || [[ "$OSTYPE" == 'linux'* ]]; then
        # shellcheck disable=SC2016
        PATH_STRING='export PATH="$HOME/.local/bin:$PATH"'
        mkdir -p "$HOME/.local/bin"
        mkdir -p "${HOME}/.local/lib"

        if ! grep "$PATH_STRING" < "$HOME/.profile" > /dev/null; then
            echo -e "${PATH_STRING}\n" >> "$HOME/.profile"
            logger info "Updated the PATH variable to include ~/.local/bin in $HOME/.profile"
        fi
        elif [[ "$OSTYPE" == 'cygwin' ]] || [[ "$OSTYPE" == 'msys' ]] || [[ "$OSTYPE" == 'win32' ]]; then
        logger error "Windows is not directly supported. Use WSL or Docker." && exit 1
        elif [[ "$OSTYPE" == 'freebsd'* ]]; then
        logger error "FreeBSD support not added yet" && exit 1
    else
        logger warn "System type not recognized"
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

# @description Helper function for ensureTaskInstalled that performs the installation of Task.
#
# @see ensureTaskInstalled
#
# @noarg
#
# @exitcode 0 If Task installs/updates properly
# @exitcode 1+ If the installation fails
function installTask() {
    # @description Release URL to use when downloading [Task](https://github.com/go-task/task)
    TASK_RELEASE_URL="https://github.com/go-task/task/releases/latest"
    CHECKSUM_DESTINATION=/tmp/megabytelabs/task_checksums.txt
    CHECKSUMS_URL="$TASK_RELEASE_URL/download/task_checksums.txt"
    DOWNLOAD_DESTINATION=/tmp/megabytelabs/task.tar.gz
    TMP_DIR=/tmp/megabytelabs
    logger info "Checking if install target is macOS or Linux"
    if [[ "$OSTYPE" == 'darwin'* ]]; then
        DOWNLOAD_URL="$TASK_RELEASE_URL/download/task_darwin_amd64.tar.gz"
    else
        DOWNLOAD_URL="$TASK_RELEASE_URL/download/task_linux_amd64.tar.gz"
    fi
    logger "Creating folder for Task download"
    mkdir -p "$(dirname "$DOWNLOAD_DESTINATION")"
    logger info "Downloading latest version of Task"
    curl -sSL "$DOWNLOAD_URL" -o "$DOWNLOAD_DESTINATION"
    curl -sSL "$CHECKSUMS_URL" -o "$CHECKSUM_DESTINATION"
    DOWNLOAD_BASENAME="$(basename "$DOWNLOAD_URL")"
    DOWNLOAD_SHA256="$(grep "$DOWNLOAD_BASENAME" < "$CHECKSUM_DESTINATION" | cut -d ' ' -f 1)"
    sha256 "$DOWNLOAD_DESTINATION" "$DOWNLOAD_SHA256" > /dev/null
    logger success "Validated checksum"
    mkdir -p "$TMP_DIR/task"
    tar -xzf "$DOWNLOAD_DESTINATION" -C "$TMP_DIR/task" > /dev/null
    if type task &> /dev/null && [ -w "$(which task)" ]; then
        TARGET_BIN_DIR="."
        TARGET_DEST="$(which task)"
    else
        if [ "$USER" == "root" ] || (type sudo &> /dev/null && sudo -n true); then
            TARGET_BIN_DIR='/usr/local/bin'
        else
            TARGET_BIN_DIR="$HOME/.local/bin"
        fi
        TARGET_DEST="$TARGET_BIN_DIR/task"
    fi
    if [ "$USER" == "root" ]; then
        mkdir -p "$TARGET_BIN_DIR"
        mv "$TMP_DIR/task/task" "$TARGET_DEST"
        elif type sudo &> /dev/null && sudo -n true; then
        sudo mkdir -p "$TARGET_BIN_DIR"
        sudo mv "$TMP_DIR/task/task" "$TARGET_DEST"
    else
        mkdir -p "$TARGET_BIN_DIR"
        mv "$TMP_DIR/task/task" "$TARGET_DEST"
    fi
    logger success "Installed Task to $TARGET_DEST"
    rm "$CHECKSUM_DESTINATION"
    rm "$DOWNLOAD_DESTINATION"
}

# @description Verifies the SHA256 checksum of a file
#
# @arg $1 string Path to the file
# @arg $2 string The SHA256 signature
#
# @exitcode 0 The checksum is valid or the system is unrecognized
# @exitcode 1+ The OS is unsupported or if the checksum is invalid
function sha256() {
    if [[ "$OSTYPE" == 'darwin'* ]]; then
        if type brew &> /dev/null && ! type sha256sum &> /dev/null; then
            brew install coreutils
        else
            logger warn "Brew is not installed - this may cause issues"
        fi
        if type brew &> /dev/null; then
            PATH="$(brew --prefix)/opt/coreutils/libexec/gnubin:$PATH"
        fi
        if type sha256sum &> /dev/null; then
            echo "$2 $1" | sha256sum -c
        else
            logger warn "Checksum validation is being skipped for $1 because the sha256sum program is not available"
        fi
        elif [[ "$OSTYPE" == 'linux-gnu'* ]]; then
        if ! type shasum &> /dev/null; then
            logger warn "Checksum validation is being skipped for $1 because the shasum program is not installed"
        else
            echo "$2  $1" | shasum -s -a 256 -c
        fi
        elif [[ "$OSTYPE" == 'linux-musl' ]]; then
        if ! type sha256sum &> /dev/null; then
            logger warn "Checksum validation is being skipped for $1 because the sha256sum program is not available"
        else
            echo "$2  $1" | sha256sum -c
        fi
        elif [[ "$OSTYPE" == 'cygwin' ]] || [[ "$OSTYPE" == 'msys' ]] || [[ "$OSTYPE" == 'win32' ]]; then
        logger error "Windows is not directly supported. Use WSL or Docker." && exit 1
        elif [[ "$OSTYPE" == 'freebsd'* ]]; then
        logger error "FreeBSD support not added yet" && exit 1
    else
        logger warn "System type not recognized. Skipping checksum validation."
    fi
}

##### Main Logic #####
function bootstrap_ansible_node(){
    local _username=${1:-'ansible'}

    if [ ! -f "$HOME/.profile" ]; then
        touch "$HOME/.profile"
    fi

    ensure_logdir
    ensure_permissions

    # @description Ensure git hosts are all in ~/.ssh/known_hosts
    mkdir -p ~/.ssh
    chmod 700 ~/.ssh
    if [ ! -f ~/.ssh/known_hosts ]; then
        touch ~/.ssh/known_hosts
        chmod 600 ~/.ssh/known_hosts
    fi

    if ! grep -q "^gitlab.com " ~/.ssh/known_hosts; then
        ssh-keyscan gitlab.com >> ~/.ssh/known_hosts 2>/dev/null
    fi

    if ! grep -q "^github.com " ~/.ssh/known_hosts; then
        ssh-keyscan github.com >> ~/.ssh/known_hosts 2>/dev/null
    fi

    if ! grep -q "^bitbucket.org " ~/.ssh/known_hosts; then
        ssh-keyscan bitbucket.org >> ~/.ssh/known_hosts 2>/dev/null
    fi

    # @description Ensures ~/.local/bin is in PATH
    ensureLocalPath

    # @description Ensures base dependencies are installed
    if [[ "$OSTYPE" == 'darwin'* ]]; then
        if ! type curl &> /dev/null && type brew &> /dev/null; then
            brew install curl
        fi
        if ! type git &> /dev/null; then
            # shellcheck disable=SC2016
            logger info 'Git is not present. A password may be required to run sudo xcode-select --install'
            sudo xcode-select --install
        fi
        elif [[ "$OSTYPE" == 'linux-gnu'* ]] || [[ "$OSTYPE" == 'linux-musl'* ]]; then
        if ! type curl &> /dev/null || ! type git &> /dev/null || ! type gzip &> /dev/null || ! type sudo &> /dev/null || ! type jq &> /dev/null; then
            ensurePackageInstalled "curl"
            ensurePackageInstalled "file"
            ensurePackageInstalled "git"
            ensurePackageInstalled "gzip"
            ensurePackageInstalled "sudo"
            ensurePackageInstalled "jq"
            ensurePackageInstalled "rsync"
        fi
    fi

    # @description Ensures Homebrew, Poetry, and Volta are installed
    if [ -z "$NO_INSTALL_HOMEBREW" ]; then
        if [[ "$OSTYPE" == 'darwin'* ]] || [[ "$OSTYPE" == 'linux-gnu'* ]] || [[ "$OSTYPE" == 'linux-musl'* ]]; then
            if [ -z "$INIT_CWD" ]; then
                if ! type brew &> /dev/null; then
                    if type sudo &> /dev/null && sudo -n true; then

                        echo | /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
                    else
                        logger warn "Homebrew is not installed. The script will attempt to install Homebrew and you might be prompted for your password."
                        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" || BREW_EXIT_CODE="$?"

                        if [ -n "$BREW_EXIT_CODE" ]; then
                            if command -v brew > /dev/null; then
                                "${XDG_DATA_HOME}/logger.sh" warn "Homebrew was installed but part of the installation failed. Retrying again after changing a few things.."

                                BREW_DIRS="share/man share/doc share/zsh/site-functions etc/bash_completion.d"
                                for BREW_DIR in $BREW_DIRS; do
                                    if [ -d "$(brew --prefix)/$BREW_DIR" ]; then
                                        sudo chown -R "$(whoami)" "$(brew --prefix)/$BREW_DIR"

                                    fi
                                done
                                brew update --force --quiet
                            fi
                        fi
                    fi
                fi
                if ! (grep "/bin/brew shellenv" < "$HOME/.profile" &> /dev/null) && [[ "$OSTYPE" != 'darwin'* ]]; then

                    # shellcheck disable=SC2016
                    logger info 'Adding linuxbrew source command to ~/.profile'

                    # shellcheck disable=SC2016
                    echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> "$HOME/.profile"

                fi
                if [ -f "$HOME/.profile" ]; then
                    # shellcheck disable=SC1091
                    . "$HOME/.profile" &> /dev/null || true
                fi
                if ! type poetry &> /dev/null; then
                    # shellcheck disable=SC2016
                    brew install poetry || logger info 'There may have been an issue installing poetry with brew'
                fi
                if ! type jq &> /dev/null; then
                    # shellcheck disable=SC2016
                    brew install jq || logger info 'There may have been an issue installiny jq with brew'
                fi
                if ! type yq &> /dev/null; then
                    # shellcheck disable=SC2016
                    brew install yq || logger info 'There may have been an issue installing yq with brew'
                fi
            fi
        fi
    fi

}

