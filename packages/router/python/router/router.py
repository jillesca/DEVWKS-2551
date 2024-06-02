# -*- mode: python; python-indent: 4 -*-
import ncs
from ncs.application import Service


class ServiceCallbacks(Service):

    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        self.log.info("Service create(service=", service._path, ")")
        if service.sys.dns:
            for server in service.sys.dns.server:
                vars = ncs.template.Variables()
                vars.add("DNS_ADDRESS", server.address)
                template = ncs.template.Template(service)
                template.apply("dns-template", vars)

        if service.sys.syslog:
            for server in service.sys.syslog.server:
                vars = ncs.template.Variables()
                vars.add("SYSLOG_ADDRESS", server.name)
                template = ncs.template.Template(service)
                template.apply("syslog-template", vars)


class Router(ncs.application.Application):
    def setup(self):
        self.log.info("Router RUNNING")
        self.register_service("router-servicepoint", ServiceCallbacks)

    def teardown(self):
        self.log.info("Router FINISHED")
