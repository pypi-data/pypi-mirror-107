# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from .cache_policy import *
from .distribution import *
from .function import *
from .get_cache_policy import *
from .get_distribution import *
from .get_origin_request_policy import *
from .key_group import *
from .origin_access_identity import *
from .origin_request_policy import *
from .public_key import *
from .realtime_log_config import *
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
            if typ == "aws:cloudfront/cachePolicy:CachePolicy":
                return CachePolicy(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "aws:cloudfront/distribution:Distribution":
                return Distribution(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "aws:cloudfront/function:Function":
                return Function(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "aws:cloudfront/keyGroup:KeyGroup":
                return KeyGroup(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "aws:cloudfront/originAccessIdentity:OriginAccessIdentity":
                return OriginAccessIdentity(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "aws:cloudfront/originRequestPolicy:OriginRequestPolicy":
                return OriginRequestPolicy(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "aws:cloudfront/publicKey:PublicKey":
                return PublicKey(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "aws:cloudfront/realtimeLogConfig:RealtimeLogConfig":
                return RealtimeLogConfig(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("aws", "cloudfront/cachePolicy", _module_instance)
    pulumi.runtime.register_resource_module("aws", "cloudfront/distribution", _module_instance)
    pulumi.runtime.register_resource_module("aws", "cloudfront/function", _module_instance)
    pulumi.runtime.register_resource_module("aws", "cloudfront/keyGroup", _module_instance)
    pulumi.runtime.register_resource_module("aws", "cloudfront/originAccessIdentity", _module_instance)
    pulumi.runtime.register_resource_module("aws", "cloudfront/originRequestPolicy", _module_instance)
    pulumi.runtime.register_resource_module("aws", "cloudfront/publicKey", _module_instance)
    pulumi.runtime.register_resource_module("aws", "cloudfront/realtimeLogConfig", _module_instance)

_register_module()
