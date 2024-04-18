#!/usr/bin/env zsh

poetry run ./dbs update-collections &&
poetry run ./dbs update-roles &&
poetry run ./dbs destroy --app-name lxc &&
poetry run ./dbs create --app-name lxc &&
poetry run ./dbs destroy --app-name lxc &&
poetry run ./dbs update-facts