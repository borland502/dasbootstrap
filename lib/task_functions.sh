# Taken in conjunction with the task dbs:run mimics the original dbs script execution
# e.g. dbs
function dbs_run(){
    task -t "${HOME}/Taskfile.yml" dbs:run "--help"
}

function get_confirmed_path() {
    local path
    
    while true; do
        path=$(gum prompt "Enter path: ")
        
        if [[ -d "$path" ]]; then  # Check if directory exists
            gum echo "You entered: $path"
            if gum confirm "Is this path correct?"; then
                return 0  # Success, path confirmed
            fi
        else
            gum echo "Path does not exist. Please try again."
        fi
    done
};