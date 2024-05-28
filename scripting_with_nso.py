from pprint import pprint as pp
import ncs


def see_devices_attributes() -> None:
    maapi = ncs.maapi.Maapi()
    maapi.start_user_session(user="admin", context="system", groups=[])
    transaction = maapi.start_write_trans()

    root = ncs.maagic.get_root(backend=transaction)
    for device in root.devices.device:
        if "core-rtr" in device.name:
            pp(dir(device))
    maapi.close()


def see_device_address() -> None:
    maapi = ncs.maapi.Maapi()
    maapi.start_user_session(user="admin", context="system", groups=[])
    transaction = maapi.start_write_trans()

    root = ncs.maagic.get_root(backend=transaction)
    for device in root.devices.device:
        print(f"Device {device.name} address {device.address}")
    maapi.close()


def update_device_attribute_dry_run(device_name: str, hostname: str) -> dict:
    with ncs.maapi.single_write_trans(
        user="admin", context="system"
    ) as transaction:
        root = ncs.maagic.get_root(backend=transaction)
        root.devices.device[device_name].config.hostname = hostname

        commit_params = transaction.get_params()
        commit_params.dry_run_native()
        dry_run_result = transaction.apply_params(
            keep_open=True, params=commit_params
        )
        print(f"{dry_run_result=}")


def update_device_attribute(device_name: str, hostname: str) -> None:
    with ncs.maapi.single_write_trans(
        user="admin", context="system"
    ) as transaction:
        root = ncs.maagic.get_root(backend=transaction)
        root.devices.device[device_name].config.hostname = hostname
        transaction.apply()


def show_xr_command(device_name: str, command: str):
    with ncs.maapi.start_user_session(
        user="admin", context="system", groups=[]
    ) as transaction:
        root = ncs.maagic.get_root(backend=transaction)
        device = root.devices.device[device_name]
        device.live_status.cisco_ios_xr_stats__exec(command)
        transaction.apply()


if "__main__" == __name__:
    see_devices_attributes()
    # see_device_address()
    # update_device_attribute_dry_run(device_name="core-rtr0", hostname="devwks-2551")
    # update_device_attribute(device_name="core-rtr0", hostname="devwks-2551")
