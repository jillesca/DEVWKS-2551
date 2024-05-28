from pprint import pprint as pp
import ncs


def see_devices_attributes():
    maapi = ncs.maapi.Maapi()
    maapi.start_user_session(user="admin", context="system", groups=[])
    transaction = maapi.start_write_trans()
    root = ncs.maagic.get_root(transaction)
    for device in root.devices.device:
        pp(dir(device))
    maapi.close()


def see_device_address():
    maapi = ncs.maapi.Maapi()
    maapi.start_user_session(user="admin", context="system", groups=[])
    transaction = maapi.start_write_trans()
    root = ncs.maagic.get_root(transaction)
    for device in root.devices.device:
        print(f"Device {device.name} address {device.address}")
    maapi.close()


def update_device_attribute_dry_run(device_name: str):
    with ncs.maapi.single_write_trans(
        user="admin", context="system"
    ) as transaction:
        root = ncs.maagic.get_root(transaction)
        root.devices.device["core-rtr0"].config.hostname = device_name

        commit_params = ncs.maapi.CommitParams()
        commit_params.dry_run_native()
        dry_run_result = transaction.apply_params(
            keep_open=True, params=commit_params
        )
        print(f"{dry_run_result=}")


def update_device_attribute(device_name: str):
    with ncs.maapi.single_write_trans(
        user="admin", context="system"
    ) as transaction:
        root = ncs.maagic.get_root(transaction)
        root.devices.device["core-rtr0"].config.hostname = device_name
        transaction.apply()


if "__main__" == __name__:
    see_devices_attributes()
    # see_device_address()
    # update_device_attribute_dry_run(device_name="devwks-2551")
    # update_device_attribute(device_name="devwks-2551")
