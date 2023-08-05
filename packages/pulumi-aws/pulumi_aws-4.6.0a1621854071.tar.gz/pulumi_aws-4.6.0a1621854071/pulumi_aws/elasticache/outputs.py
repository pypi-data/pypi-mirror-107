# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'ClusterCacheNode',
    'ParameterGroupParameter',
    'ReplicationGroupClusterMode',
    'GetClusterCacheNodeResult',
]

@pulumi.output_type
class ClusterCacheNode(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "availabilityZone":
            suggest = "availability_zone"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ClusterCacheNode. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ClusterCacheNode.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ClusterCacheNode.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 address: Optional[str] = None,
                 availability_zone: Optional[str] = None,
                 id: Optional[str] = None,
                 port: Optional[int] = None):
        """
        :param str availability_zone: Availability Zone for the cache cluster. If you want to create cache nodes in multi-az, use `preferred_availability_zones` instead. Default: System chosen Availability Zone. Changing this value will re-create the resource.
        :param int port: The port number on which each of the cache nodes will accept connections. For Memcached the default is 11211, and for Redis the default port is 6379. Cannot be provided with `replication_group_id`. Changing this value will re-create the resource.
        """
        if address is not None:
            pulumi.set(__self__, "address", address)
        if availability_zone is not None:
            pulumi.set(__self__, "availability_zone", availability_zone)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if port is not None:
            pulumi.set(__self__, "port", port)

    @property
    @pulumi.getter
    def address(self) -> Optional[str]:
        return pulumi.get(self, "address")

    @property
    @pulumi.getter(name="availabilityZone")
    def availability_zone(self) -> Optional[str]:
        """
        Availability Zone for the cache cluster. If you want to create cache nodes in multi-az, use `preferred_availability_zones` instead. Default: System chosen Availability Zone. Changing this value will re-create the resource.
        """
        return pulumi.get(self, "availability_zone")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def port(self) -> Optional[int]:
        """
        The port number on which each of the cache nodes will accept connections. For Memcached the default is 11211, and for Redis the default port is 6379. Cannot be provided with `replication_group_id`. Changing this value will re-create the resource.
        """
        return pulumi.get(self, "port")


@pulumi.output_type
class ParameterGroupParameter(dict):
    def __init__(__self__, *,
                 name: str,
                 value: str):
        """
        :param str name: The name of the ElastiCache parameter.
        :param str value: The value of the ElastiCache parameter.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the ElastiCache parameter.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The value of the ElastiCache parameter.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class ReplicationGroupClusterMode(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "numNodeGroups":
            suggest = "num_node_groups"
        elif key == "replicasPerNodeGroup":
            suggest = "replicas_per_node_group"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ReplicationGroupClusterMode. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ReplicationGroupClusterMode.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ReplicationGroupClusterMode.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 num_node_groups: int,
                 replicas_per_node_group: int):
        """
        :param int num_node_groups: Number of node groups (shards) for this Redis replication group. Changing this number will trigger an online resizing operation before other settings modifications.
        :param int replicas_per_node_group: Number of replica nodes in each node group. Valid values are 0 to 5. Changing this number will trigger an online resizing operation before other settings modifications.
        """
        pulumi.set(__self__, "num_node_groups", num_node_groups)
        pulumi.set(__self__, "replicas_per_node_group", replicas_per_node_group)

    @property
    @pulumi.getter(name="numNodeGroups")
    def num_node_groups(self) -> int:
        """
        Number of node groups (shards) for this Redis replication group. Changing this number will trigger an online resizing operation before other settings modifications.
        """
        return pulumi.get(self, "num_node_groups")

    @property
    @pulumi.getter(name="replicasPerNodeGroup")
    def replicas_per_node_group(self) -> int:
        """
        Number of replica nodes in each node group. Valid values are 0 to 5. Changing this number will trigger an online resizing operation before other settings modifications.
        """
        return pulumi.get(self, "replicas_per_node_group")


@pulumi.output_type
class GetClusterCacheNodeResult(dict):
    def __init__(__self__, *,
                 address: str,
                 availability_zone: str,
                 id: str,
                 port: int):
        """
        :param str availability_zone: The Availability Zone for the cache cluster.
        :param int port: The port number on which each of the cache nodes will
               accept connections.
        """
        pulumi.set(__self__, "address", address)
        pulumi.set(__self__, "availability_zone", availability_zone)
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "port", port)

    @property
    @pulumi.getter
    def address(self) -> str:
        return pulumi.get(self, "address")

    @property
    @pulumi.getter(name="availabilityZone")
    def availability_zone(self) -> str:
        """
        The Availability Zone for the cache cluster.
        """
        return pulumi.get(self, "availability_zone")

    @property
    @pulumi.getter
    def id(self) -> str:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def port(self) -> int:
        """
        The port number on which each of the cache nodes will
        accept connections.
        """
        return pulumi.get(self, "port")


