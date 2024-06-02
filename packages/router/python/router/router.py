# -*- mode: python; python-indent: 4 -*-
import ncs
from ncs.application import Service


class ServiceCallbacks(Service):

    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        self.log.info("Service create(service=", service._path, ")")

        self.log.debug(f"{dir(service)=}")
        self.log.debug(f"{type(service)=}")
        self.log.debug(f"{dir(service.sys)=}")
        self.log.debug(f"{dir(service.sys.dns)=}")
        self.log.debug(f"{type(service.sys.dns)=}")
        self.log.debug(f"{service.sys.dns=}")
        self.log.debug(f"{service.sys.dns.server=}")
        self.log.debug(f"{dir(service.sys.dns.server)=}")
        for server in service.sys.dns.server:
            self.log.debug(f"loop for server")
            self.log.debug(f"{server=}")
            self.log.debug(f"{dir(server)=}")
            self.log.debug(f"{type(server)=}")
            vars = ncs.template.Variables()
            vars.add("IP_ADDRESS", server.address)
            template = ncs.template.Template(service)
            template.apply("dns-template", vars)


class Router(ncs.application.Application):
    def setup(self):
        self.log.info("Router RUNNING")
        self.register_service("router-servicepoint", ServiceCallbacks)

    def teardown(self):
        self.log.info("Router FINISHED")
