# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from .domain import *
from .instance import *
from .instance_public_ports import *
from .key_pair import *
from .static_ip import *
from .static_ip_attachment import *
from ._inputs import *
from . import outputs

def _register_module():
    import pulumi
    from .. import _utilities


    class Module(pulumi.runtime.ResourceModule):
        _version = _utilities.get_semver_version()

        def version(self):
            return Module._version

        def construct(self, name: str, typ: str, urn: str) -> pulumi.Resource:
            if typ == "aws:lightsail/domain:Domain":
                return Domain(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "aws:lightsail/instance:Instance":
                return Instance(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "aws:lightsail/instancePublicPorts:InstancePublicPorts":
                return InstancePublicPorts(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "aws:lightsail/keyPair:KeyPair":
                return KeyPair(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "aws:lightsail/staticIp:StaticIp":
                return StaticIp(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "aws:lightsail/staticIpAttachment:StaticIpAttachment":
                return StaticIpAttachment(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("aws", "lightsail/domain", _module_instance)
    pulumi.runtime.register_resource_module("aws", "lightsail/instance", _module_instance)
    pulumi.runtime.register_resource_module("aws", "lightsail/instancePublicPorts", _module_instance)
    pulumi.runtime.register_resource_module("aws", "lightsail/keyPair", _module_instance)
    pulumi.runtime.register_resource_module("aws", "lightsail/staticIp", _module_instance)
    pulumi.runtime.register_resource_module("aws", "lightsail/staticIpAttachment", _module_instance)

_register_module()
