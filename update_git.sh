#!/bin/bash
# Author : Arnaud MENG

# Functions --------------------------------------------------------------------

# This function uses date to generate unique commit name each second
function generate_commit_name
{
    commit_name=$(date '+%d%m%Y-%X')
    echo $commit_name
}

# Definitions and working path setting -----------------------------------------

# Defining local project directory 
local_repository="/home/meng/Pipeline"

# Defining remote repository adress
remote_repository="https://github.com/arnaudmeng/denovo-assembly-pipeline-upmc.git"

# Defining local files to be update
config_file="config.xml"
pipeline_script="pipeline.py"
modules_directory="./src"
update_git_script="update_git.sh"
readme_git="README.git"

# Move to $local_repository location
cd $local_repository

# Launching Git commands to update remote repository ---------------------------

# Adding files to be update
eval "git add $config_file"
eval "git add $pipeline_script"
eval "git add $modules_directory"
eval "git add $update_git_script"
eval "git add $readme_git"

# Setting remote URL repository
eval "git remote set-url origin $remote_repository"

# Generating commit unique name
commitname=$(generate_commit_name)
eval  "git commit -m '$commitname'"

# Updating remote repository
eval "git push origin master"

