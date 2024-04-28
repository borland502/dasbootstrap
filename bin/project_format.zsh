#!/usr/bin/env zsh

# shellcheck disable=SC2046
pyupgrade --py311-plus $(find pyprojects/**/*.py)
pyright pyprojects shared
ruff check pyprojects shared --config pyproject.toml --fix\
 && ruff format ./pyprojects ./shared --config pyproject.toml --line-length 128 --target-version py311