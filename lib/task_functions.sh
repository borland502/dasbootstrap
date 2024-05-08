# Taken in conjunction with the task dbs:run mimics the original dbs script execution
# e.g. dbs
function dbs_run(){
    task -t "${HOME}/Taskfile.yml" dbs:run "--help"
}

