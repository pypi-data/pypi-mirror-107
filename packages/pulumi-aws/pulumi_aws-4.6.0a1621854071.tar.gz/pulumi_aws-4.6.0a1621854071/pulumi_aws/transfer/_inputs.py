# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'ServerEndpointDetailsArgs',
    'UserHomeDirectoryMappingArgs',
]

@pulumi.input_type
class ServerEndpointDetailsArgs:
    def __init__(__self__, *,
                 address_allocation_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 subnet_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 vpc_endpoint_id: Optional[pulumi.Input[str]] = None,
                 vpc_id: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[Sequence[pulumi.Input[str]]] address_allocation_ids: A list of address allocation IDs that are required to attach an Elastic IP address to your SFTP server's endpoint. This property can only be used when `endpoint_type` is set to `VPC`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] subnet_ids: A list of subnet IDs that are required to host your SFTP server endpoint in your VPC. This property can only be used when `endpoint_type` is set to `VPC`.
        :param pulumi.Input[str] vpc_endpoint_id: The ID of the VPC endpoint. This property can only be used when `endpoint_type` is set to `VPC_ENDPOINT`
        :param pulumi.Input[str] vpc_id: The VPC ID of the virtual private cloud in which the SFTP server's endpoint will be hosted. This property can only be used when `endpoint_type` is set to `VPC`.
        """
        if address_allocation_ids is not None:
            pulumi.set(__self__, "address_allocation_ids", address_allocation_ids)
        if subnet_ids is not None:
            pulumi.set(__self__, "subnet_ids", subnet_ids)
        if vpc_endpoint_id is not None:
            pulumi.set(__self__, "vpc_endpoint_id", vpc_endpoint_id)
        if vpc_id is not None:
            pulumi.set(__self__, "vpc_id", vpc_id)

    @property
    @pulumi.getter(name="addressAllocationIds")
    def address_allocation_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of address allocation IDs that are required to attach an Elastic IP address to your SFTP server's endpoint. This property can only be used when `endpoint_type` is set to `VPC`.
        """
        return pulumi.get(self, "address_allocation_ids")

    @address_allocation_ids.setter
    def address_allocation_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "address_allocation_ids", value)

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of subnet IDs that are required to host your SFTP server endpoint in your VPC. This property can only be used when `endpoint_type` is set to `VPC`.
        """
        return pulumi.get(self, "subnet_ids")

    @subnet_ids.setter
    def subnet_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "subnet_ids", value)

    @property
    @pulumi.getter(name="vpcEndpointId")
    def vpc_endpoint_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the VPC endpoint. This property can only be used when `endpoint_type` is set to `VPC_ENDPOINT`
        """
        return pulumi.get(self, "vpc_endpoint_id")

    @vpc_endpoint_id.setter
    def vpc_endpoint_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vpc_endpoint_id", value)

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> Optional[pulumi.Input[str]]:
        """
        The VPC ID of the virtual private cloud in which the SFTP server's endpoint will be hosted. This property can only be used when `endpoint_type` is set to `VPC`.
        """
        return pulumi.get(self, "vpc_id")

    @vpc_id.setter
    def vpc_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vpc_id", value)


@pulumi.input_type
class UserHomeDirectoryMappingArgs:
    def __init__(__self__, *,
                 entry: pulumi.Input[str],
                 target: pulumi.Input[str]):
        """
        :param pulumi.Input[str] entry: Represents an entry and a target.
        :param pulumi.Input[str] target: Represents the map target.
        """
        pulumi.set(__self__, "entry", entry)
        pulumi.set(__self__, "target", target)

    @property
    @pulumi.getter
    def entry(self) -> pulumi.Input[str]:
        """
        Represents an entry and a target.
        """
        return pulumi.get(self, "entry")

    @entry.setter
    def entry(self, value: pulumi.Input[str]):
        pulumi.set(self, "entry", value)

    @property
    @pulumi.getter
    def target(self) -> pulumi.Input[str]:
        """
        Represents the map target.
        """
        return pulumi.get(self, "target")

    @target.setter
    def target(self, value: pulumi.Input[str]):
        pulumi.set(self, "target", value)


