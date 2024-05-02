#!/usr/bin/env bash

if ! [[ ${DBS_SCROOT+x} ]]; then
  # shellcheck disable=SC2155
  declare -rx DBS_SCROOT=${HOME}/.local/share/automation/dasbootstrap
fi

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

# function bootstrap_dasbootstrap() {
#   # Iterate over GITHUB_URLS array
#   for context_path in "${!GITHUB_URLS[@]}"; do
#     # Get the corresponding URL
#     url="${GITHUB_URLS[$context_path]}"

#     # Extract the repository name from the URL
#     repo_name=$(basename "${url%.git}")

#     # Construct the clone path
#     clone_path="${XDG_DATA_HOME}/${repo_name}"

#     # Check if the repository already exists
#     if [[ -d "${clone_path}" ]]; then
#       echo "Updating existing repository: ${repo_name}"
#       cd "${clone_path}" || { echo "Failed to cd to ${clone_path}"; continue; }
#       git fetch --all --prune || echo "Error fetching updates for ${repo_name}"
#       git reset --hard
#     else
#       # Clone the repository if it doesn't exist
#       echo "Cloning ${url} to ${clone_path}"
#       git clone "${url}" "${clone_path}" || echo "Error cloning ${url}"
#     fi

#    for sh_file in "${clone_path}"/*.sh; do

#      if [[ -f "${sh_file}" ]]; then
#        # Get the base filename without extension
#        base_filename="$(basename "${sh_file%.sh}")"

#        # Create the symlink in XDG_BIN_HOME
#        ln -sf "${sh_file}" "${XDG_BIN_HOME}/${base_filename}" || echo "Error creating symlink for ${sh_file}"
#        chmod +x "${XDG_BIN_HOME}/${base_filename}"
#      fi

#     # done
#   done

#   echo "Finished cloning/updating repositories."
# }
