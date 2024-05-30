#!/bin/bash 


echo 'Setting environment variables'
LAB_DIR=${HOME}/src
NCS_RUN_DIR=${LAB_DIR}/workshop

echo 'alias ll="ls -al"' >> ${HOME}/.bashrc
echo LAB_DIR=${HOME}/src >> ${HOME}/.bashrc
echo NCS_RUN_DIR=${LAB_DIR}/workshop >> ${HOME}/.bashrc

echo 'Sourcing the bashrc'
source ${HOME}/.bashrc

echo 'Creating workshop directory'
mkdir -p ${LAB_DIR}
mkdir -p ${NCS_RUN_DIR}


echo 'Creating netsim devices'
ncs-netsim --dir ${NCS_RUN_DIR}/netsim create-network $NCS_DIR/packages/neds/cisco-ios-cli-3.0 1 dist-rtr
ncs-netsim --dir ${NCS_RUN_DIR}/netsim add-to-network $NCS_DIR/packages/neds/cisco-iosxr-cli-3.5 1 core-rtr

echo 'Setting up netsim'
ncs-setup --dest ${NCS_RUN_DIR} --netsim-dir ${NCS_RUN_DIR}/netsim

echo 'Creating the router package'
ncs-make-package  --no-java --service-skeleton python-and-template --component-class router.Router --dest ${NCS_RUN_DIR}/packages/router router

echo 'start netsim devices'
cd ${NCS_RUN_DIR}
ncs-netsim start

echo 'start ncs'
ncs

echo 'ncs status'
ncs --status | grep -i status

echo 'sycn devices'
echo "devices sync-from" | ncs_cli -C -u admin
