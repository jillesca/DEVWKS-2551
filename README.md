# Empowering Network Automation

Welcome to **DEVWKS-2551 Empowering Network Automation, Practice NSO with Python**

On this file you can find the instructions to work during the workshop. However, you can try the exercise presented here at any time using the **_Cisco Cloud IDE Run it!_** button on the top left corner.

For reference, you can find the info shared on the workshop under the [NSO Python API](NSO_Python_API.md) markdown file.

## Setup the environment

Setup the environment required for the lab.

```bash
make
```

> [!NOTE]
> If you receive an error during the setup, enter `make` again. If there are too many issues, reset the environment.

## Scenario 1. Scripting with the NSO Python API

Examine the examples show on the [ncs_scripting.py file](scripting/ncs_scripting.py)

Run the python scripts and review the output.

```bash
python ~/src/scripting/ncs_scripting.py
```

## Scenario 2. Run services with NSO Python API

First compile the package used.

```bash
make clean all -C ${NCS_RUN_DIR}/packages/router/src/
```

Reload the packages.

```bash
echo "packages reload" | ncs_cli -C -u admin
```

Test the package

```bash
ncs_cli -Cu admin
config
```

Pick any of the lines below to test the package

```bash
router core device core-rtr0 sys dns server 1.1.1.1
router core device core-rtr0 sys syslog server 1.1.1.1
router core device core-rtr0 sys syslog server 2.2.2.2
router core device core-rtr0 sys ntp server 1.1.1.1
router core device core-rtr0 sys ntp server 2.2.2.2
router distribution device dist-rtr0 sys dns server 6.6.6.6
router distribution device dist-rtr0 sys dns server 5.5.5.5
router distribution device dist-rtr0 sys syslog server 6.6.6.6
router access device dist-sw0 sys dns server 4.4.4.4
router access device dist-sw0 sys dns server 3.3.3.3
router access device dist-sw0 sys syslog server 4.4.4.4
router access device dist-sw0 sys syslog server 3.3.3.3
router access device dist-sw0 sys ntp server 4.4.4.4
router access device dist-sw0 sys ntp server 3.3.3.3
```

See the dry-run

```bash
commit dry-run
```

Commit the changes.

```bash
commit
```

## Scenario 3. Interact with NSO programmatically

Add a new DNS server using the `router` package.

Use the [restconf_service.py](scripting/restconf_service.py) file.

```bash
python ~/src/scripting/restconf_service.py
```

## Bonus. Development

This exercise was developed using the official NSO container. The [compose file](docker-compose.yml) used for development is kept for reference and is not part of the workshop.

### Useful commands

Access netsim cli device.

```bash
ncs-netsim cli-c core-rtr0 --dir ~/src/workshop/netsim
show running-config hostname
```

Use show commands using live-status on NSO.

```bash
devices device core-rtr0 live-status exec show running-config hostname
```

Redeploy the router packages for changes on python code or templates files.

```bash
echo 'packages package router redeploy' | ncs_cli -Cu admin
```
