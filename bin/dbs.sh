#!/usr/bin/env bash

###
# Wrapper script around taskfile binary for executing common dasbootstrap actions.  Assumes installation and full
# XDG_ spec availability
###

source "${XDG_DATA_LIB}/functions.sh"

# TODO: alias task functions in chezmoi managed .zshrc files and discard this script

# Taken in conjection with the task dbs:runm mimics the original dbs script execution
# e.g. dbs
function dbs(){
    task -t Taskfile.yml dbs:run -- $@
}