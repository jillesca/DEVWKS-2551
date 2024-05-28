# Empowering Network Automation

Welcome to **DEVWKS-2551 Empowering Network Automation, Practice NSO with Python**

On this file you can find the instructions to work during the workshop. However, you can try the exercise presented here at any time using the **_Cisco Cloud IDE Run it!_** button on the top left corner.

For reference, you can find the info shared on the workshop under the [NSO Python API](NSO_Python_API.md) markdown file.

## Setup the environment

Create the environment variables required for the lab to run

```bash
export LAB_DIR=${HOME}/src
mkdir -p ${LAB_DIR}
export NCS_RUN_DIR=${LAB_DIR}/nso-instance
mkdir -p ${NCS_RUN_DIR}
cd ${LAB_DIR}
```

Create the netsim devices.

```bash
ncs-netsim --dir ${NCS_RUN_DIR}/netsim create-network $NCS_DIR/packages/neds/cisco-ios-cli-3.0 1 dist-rtr
ncs-netsim --dir ${NCS_RUN_DIR}/netsim add-to-network $NCS_DIR/packages/neds/cisco-iosxr-cli-3.5 1 core-rtr
```

Set up an NSO instance (project) directory:

```bash
ncs-setup --dest ${NCS_RUN_DIR} --netsim-dir ${NCS_RUN_DIR}/netsim
```

Start netsim and NSO

```bash
cd ${NCS_RUN_DIR}
ncs-netsim start
ncs
```
