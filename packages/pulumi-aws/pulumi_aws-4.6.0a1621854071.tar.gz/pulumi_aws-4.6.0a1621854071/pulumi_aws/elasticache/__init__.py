# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from .cluster import *
from .get_cluster import *
from .get_replication_group import *
from .global_replication_group import *
from .parameter_group import *
from .replication_group import *
from .security_group import *
from .subnet_group import *
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
            if typ == "aws:elasticache/cluster:Cluster":
                return Cluster(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "aws:elasticache/globalReplicationGroup:GlobalReplicationGroup":
                return GlobalReplicationGroup(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "aws:elasticache/parameterGroup:ParameterGroup":
                return ParameterGroup(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "aws:elasticache/replicationGroup:ReplicationGroup":
                return ReplicationGroup(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "aws:elasticache/securityGroup:SecurityGroup":
                return SecurityGroup(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "aws:elasticache/subnetGroup:SubnetGroup":
                return SubnetGroup(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("aws", "elasticache/cluster", _module_instance)
    pulumi.runtime.register_resource_module("aws", "elasticache/globalReplicationGroup", _module_instance)
    pulumi.runtime.register_resource_module("aws", "elasticache/parameterGroup", _module_instance)
    pulumi.runtime.register_resource_module("aws", "elasticache/replicationGroup", _module_instance)
    pulumi.runtime.register_resource_module("aws", "elasticache/securityGroup", _module_instance)
    pulumi.runtime.register_resource_module("aws", "elasticache/subnetGroup", _module_instance)

_register_module()
