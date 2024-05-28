import ncs

with ncs.maapi.Maapi() as m:
    with ncs.maapi.Session(m, "admin", "python", groups=["ncsadmin"]):
        with m.start_write_trans() as t_rw:

            root = ncs.maagic.get_root(t_rw)
            device_cdb = root.devices.device["eng04-cleaf-02"]
            device_cdb.config.interface.loopback[0].description = (
                "Done from python API"
            )

            # Starting dry-run
            cp = ncs.maapi.ConfigParams()
            cp.dry_run_native()
            dry_run_result = t_rw.apply_params(True, cp)
