#!/usr/bin/env zsh

curr_dir=$(pwd)
poe format
poe "test"
poetry build-project

cd "$curr_dir" || exit 2

cd pyprojects/semaphore_client || exit 2
poe "test"
poetry build-project

