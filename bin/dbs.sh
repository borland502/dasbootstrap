#!/usr/bin/env bash

###
# Wrapper script around taskfile binary for executing common dasbootstrap actions.  Assumes installation and full
# XDG_ spec availability
###

# TODO: alias task functions in chezmoi managed .zshrc files and discard this script

# function dbs_task(){
#    task -t Taskfile.yml dbs:run -- create --app-name 'lxc'
# }