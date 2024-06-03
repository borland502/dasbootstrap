#!/usr/bin/env zsh

if has apt; then
    sudo apt update && sudo apt dist-upgrade -y
fi

#Homebrew update and prune outdated cache
if [[ $(command -v brew) ]]; then
    brew update
    brew upgrade
    brew cleanup -s
    
    #now diagnostic
    brew doctor
    brew missing
fi

if [[ $(command -v npm) ]]; then
    # NPM global update
    npm update -g
    npm install -g npm
fi

if [[ $(command -v tldr) ]]; then
    # misc updates
    tldr --update
fi

# OSX Specific updates
if [[ -x "$(command -v softwareupdate)" ]]; then
    softwareupdate --all --install --force
fi

if [[ "$(command -v zinit)" ]]; then
    zinit update --all
fi
