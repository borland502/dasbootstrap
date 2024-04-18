#!/usr/bin/env zsh

# shellcheck disable=SC2046
pyupgrade --py311-plus $(find pyprojects/**/*.py)
pyright pyprojects shared
ruff check --fix pyprojects shared && ruff format pyprojects shared