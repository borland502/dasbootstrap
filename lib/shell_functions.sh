#!/usr/bin/env bash

# https://blog.mphomphego.co.za/blog/2022/03/08/Note-to-self-How-to-get-a-complete-plugin-list-from-Jenkins.html
function jenkins_plugin_list() {
  JENKINS_USERNAME=jenkins
  JENKINS_TOKEN=""
  JENKINS_HOST="${JENKINS_USERNAME}:${JENKINS_TOKEN}@https://jenkins.npm.technohouser.com"

  curl -sSL "http://$JENKINS_HOST/pluginManager/api/xml?depth=1&xpath=/*/*/shortName|/*/*/version&wrapper=plugins" | perl -pe 's/.*?<shortName>([\w-]+).*?<version>([^<]+)()(<\/\w+>)+/\1 \2\n/g' | sed 's/ /:/' > ansible/tmp/plugins.txt
}