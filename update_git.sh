#!/bin/bash

function generate_commit_name
{
    commit_name=$(date '+%d%m%Y-%X')
    echo $commit_name
}

# Defining local project directory 
local_repository="/home/meng/Pipeline"

# Defining remote repository adress
remote_repository="https://github.com/arnaudmeng/denovo-assembly-pipeline-upmc.git"

# Defining local files to be update
config_file="config.xml"
pipeline_script="pipeline.py"
modules_directory="./src"
update_git_script="update_git.sh"

# Move to $local_repository location
cd $local_repository

# Launching Git commands to update remote repository
eval "git add $config_file"
eval "git add $pipeline_script"
eval "git add $modules_directory"
eval "git add $update_git_script"

eval "git remote set-url origin $remote_repository"

commitname=$(generate_commit_name)
eval  "git commit -m '$commitname'"

eval "git push origin master"
