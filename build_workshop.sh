#!/bin/bash 

set -eu # Abort the script if a command returns with a non-zero exit code or if
        # a variable name is dereferenced when the variable hasn't been set

# set and save environment variables
LAB_DIR=${HOME}/src
NCS_RUN_DIR=${LAB_DIR}/workshop

echo LAB_DIR=${HOME}/src >> /etc/environment
echo NCS_RUN_DIR=${LAB_DIR}/workshop >> /etc/environment
echo 'alias ll="ls -al"' >> $HOME/.bashrc

source /etc/environment

# Create the lab directory
mkdir -p ${LAB_DIR}
mkdir -p ${NCS_RUN_DIR}

cd ${LAB_DIR}

# start netsim devices
ncs-netsim --dir ${NCS_RUN_DIR}/netsim create-network $NCS_DIR/packages/neds/cisco-ios-cli-3.0 1 dist-rtr
ncs-netsim --dir ${NCS_RUN_DIR}/netsim add-to-network $NCS_DIR/packages/neds/cisco-iosxr-cli-3.5 1 core-rtr

# setup netsim
ncs-setup --dest ${NCS_RUN_DIR} --netsim-dir ${NCS_RUN_DIR}/netsim

# create the router package
ncs-make-package  --no-java --service-skeleton python-and-template --component-class router.Router --dest ${NCS_RUN_DIR}/packages/router router

# start netsim devices and ncs
cd ${NCS_RUN_DIR}
ncs-netsim start
ncs

# sycn devices
echo "devices sync-from" | ncs_cli -C -u admin
