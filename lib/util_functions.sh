#!/usr/bin/env bash

# shellcheck disable=2317

# https://blog.mphomphego.co.za/blog/2022/03/08/Note-to-self-How-to-get-a-complete-plugin-list-from-Jenkins.html
function jenkins_plugin_list() {
    JENKINS_USERNAME=jenkins
    JENKINS_TOKEN=""
    JENKINS_HOST="${JENKINS_USERNAME}:${JENKINS_TOKEN}@https://jenkins.npm.technohouser.com"

    curl -sSL "http://$JENKINS_HOST/pluginManager/api/xml?depth=1&xpath=/*/*/shortName|/*/*/version&wrapper=plugins" | perl -pe 's/.*?<shortName>([\w-]+).*?<version>([^<]+)()(<\/\w+>)+/\1 \2\n/g' | sed 's/ /:/' > ansible/tmp/plugins.txt
}

# https://blog.mphomphego.co.za/blog/2022/03/08/Note-to-self-How-to-get-a-complete-plugin-list-from-Jenkins.html
function jenkins_plugin_list() {
    JENKINS_USERNAME=jenkins
    JENKINS_TOKEN=""
    JENKINS_HOST="${JENKINS_USERNAME}:${JENKINS_TOKEN}@https://jenkins.npm.technohouser.com"

    curl -sSL "http://$JENKINS_HOST/pluginManager/api/xml?depth=1&xpath=/*/*/shortName|/*/*/version&wrapper=plugins" | perl -pe 's/.*?<shortName>([\w-]+).*?<version>([^<]+)()(<\/\w+>)+/\1 \2\n/g' | sed 's/ /:/' >ansible/tmp/plugins.txt
}

function extract_yaml_keys_with_structure() {
    # Get the input YAML file and output filename
    local yaml_file="${1}"
    local output_file="${2}"

    # Check for yq installation
    if ! [[ $(command -v yq) ]]; then
        echo "Error: yq is not installed. Please install it using your package manager."
        return 1
    fi

    # Validate arguments
    if [[ $# -ne 2 ]]; then
        echo "Usage: extract_yaml_keys_with_structure <yaml_file> <output_file>"
        return 1
    fi

    # Extract keys with structure using yq and append to the output file
    yq -r 'walk(if type == "map" then del(.. | select(tag != "!!str")) else . end)' "$yaml_file" >>"$output_file"
}

function extract_yaml_keys_with_structure() {
    # Get the input YAML file and output filename
    local yaml_file="${1}"
    local output_file="${2}"

    # Check for yq installation
    if ! [[ $(command -v yq) ]]; then
        echo "Error: yq is not installed. Please install it using your package manager."
        return 1
    fi

    # Validate arguments
    if [[ $# -ne 2 ]]; then
        echo "Usage: extract_yaml_keys_with_structure <yaml_file> <output_file>"
        return 1
    fi

    # Extract keys with structure using yq and append to the output file
    yq -r 'walk(if type == "map" then del(.. | select(tag != "!!str")) else . end)' "$yaml_file" >>"$output_file"
}

#
function sync_system_scripts() {
    # Copy all bin and lib files to their system homes
    rsync -avzPh "${DBS_SCROOT}/bin/" "${XDG_BIN_HOME}/"
    rsync -avzPh "${DBS_SCROOT}/lib/" "${XDG_LIB_HOME}/"
}

function debug_env() {
  printenv

  if [[ "$SHELL" == *"zsh" ]]; then
    whence -pm '*'
  else
    compgen -A function -abck
  fi
}
