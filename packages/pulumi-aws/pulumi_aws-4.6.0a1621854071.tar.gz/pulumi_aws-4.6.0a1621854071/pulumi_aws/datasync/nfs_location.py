# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = ['NfsLocationArgs', 'NfsLocation']

@pulumi.input_type
class NfsLocationArgs:
    def __init__(__self__, *,
                 on_prem_config: pulumi.Input['NfsLocationOnPremConfigArgs'],
                 server_hostname: pulumi.Input[str],
                 subdirectory: pulumi.Input[str],
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a NfsLocation resource.
        :param pulumi.Input['NfsLocationOnPremConfigArgs'] on_prem_config: Configuration block containing information for connecting to the NFS File System.
        :param pulumi.Input[str] server_hostname: Specifies the IP address or DNS name of the NFS server. The DataSync Agent(s) use this to mount the NFS server.
        :param pulumi.Input[str] subdirectory: Subdirectory to perform actions as source or destination. Should be exported by the NFS server.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value pairs of resource tags to assign to the DataSync Location. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider .
        """
        pulumi.set(__self__, "on_prem_config", on_prem_config)
        pulumi.set(__self__, "server_hostname", server_hostname)
        pulumi.set(__self__, "subdirectory", subdirectory)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)

    @property
    @pulumi.getter(name="onPremConfig")
    def on_prem_config(self) -> pulumi.Input['NfsLocationOnPremConfigArgs']:
        """
        Configuration block containing information for connecting to the NFS File System.
        """
        return pulumi.get(self, "on_prem_config")

    @on_prem_config.setter
    def on_prem_config(self, value: pulumi.Input['NfsLocationOnPremConfigArgs']):
        pulumi.set(self, "on_prem_config", value)

    @property
    @pulumi.getter(name="serverHostname")
    def server_hostname(self) -> pulumi.Input[str]:
        """
        Specifies the IP address or DNS name of the NFS server. The DataSync Agent(s) use this to mount the NFS server.
        """
        return pulumi.get(self, "server_hostname")

    @server_hostname.setter
    def server_hostname(self, value: pulumi.Input[str]):
        pulumi.set(self, "server_hostname", value)

    @property
    @pulumi.getter
    def subdirectory(self) -> pulumi.Input[str]:
        """
        Subdirectory to perform actions as source or destination. Should be exported by the NFS server.
        """
        return pulumi.get(self, "subdirectory")

    @subdirectory.setter
    def subdirectory(self, value: pulumi.Input[str]):
        pulumi.set(self, "subdirectory", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value pairs of resource tags to assign to the DataSync Location. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider .
        """
        return pulumi.get(self, "tags_all")

    @tags_all.setter
    def tags_all(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags_all", value)


@pulumi.input_type
class _NfsLocationState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 on_prem_config: Optional[pulumi.Input['NfsLocationOnPremConfigArgs']] = None,
                 server_hostname: Optional[pulumi.Input[str]] = None,
                 subdirectory: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 uri: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering NfsLocation resources.
        :param pulumi.Input[str] arn: Amazon Resource Name (ARN) of the DataSync Location.
        :param pulumi.Input['NfsLocationOnPremConfigArgs'] on_prem_config: Configuration block containing information for connecting to the NFS File System.
        :param pulumi.Input[str] server_hostname: Specifies the IP address or DNS name of the NFS server. The DataSync Agent(s) use this to mount the NFS server.
        :param pulumi.Input[str] subdirectory: Subdirectory to perform actions as source or destination. Should be exported by the NFS server.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value pairs of resource tags to assign to the DataSync Location. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider .
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if on_prem_config is not None:
            pulumi.set(__self__, "on_prem_config", on_prem_config)
        if server_hostname is not None:
            pulumi.set(__self__, "server_hostname", server_hostname)
        if subdirectory is not None:
            pulumi.set(__self__, "subdirectory", subdirectory)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)
        if uri is not None:
            pulumi.set(__self__, "uri", uri)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        Amazon Resource Name (ARN) of the DataSync Location.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="onPremConfig")
    def on_prem_config(self) -> Optional[pulumi.Input['NfsLocationOnPremConfigArgs']]:
        """
        Configuration block containing information for connecting to the NFS File System.
        """
        return pulumi.get(self, "on_prem_config")

    @on_prem_config.setter
    def on_prem_config(self, value: Optional[pulumi.Input['NfsLocationOnPremConfigArgs']]):
        pulumi.set(self, "on_prem_config", value)

    @property
    @pulumi.getter(name="serverHostname")
    def server_hostname(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the IP address or DNS name of the NFS server. The DataSync Agent(s) use this to mount the NFS server.
        """
        return pulumi.get(self, "server_hostname")

    @server_hostname.setter
    def server_hostname(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "server_hostname", value)

    @property
    @pulumi.getter
    def subdirectory(self) -> Optional[pulumi.Input[str]]:
        """
        Subdirectory to perform actions as source or destination. Should be exported by the NFS server.
        """
        return pulumi.get(self, "subdirectory")

    @subdirectory.setter
    def subdirectory(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "subdirectory", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value pairs of resource tags to assign to the DataSync Location. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider .
        """
        return pulumi.get(self, "tags_all")

    @tags_all.setter
    def tags_all(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags_all", value)

    @property
    @pulumi.getter
    def uri(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "uri")

    @uri.setter
    def uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "uri", value)


class NfsLocation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 on_prem_config: Optional[pulumi.Input[pulumi.InputType['NfsLocationOnPremConfigArgs']]] = None,
                 server_hostname: Optional[pulumi.Input[str]] = None,
                 subdirectory: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Manages an NFS Location within AWS DataSync.

        > **NOTE:** The DataSync Agents must be available before creating this resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.datasync.NfsLocation("example",
            server_hostname="nfs.example.com",
            subdirectory="/exported/path",
            on_prem_config=aws.datasync.NfsLocationOnPremConfigArgs(
                agent_arns=[aws_datasync_agent["example"]["arn"]],
            ))
        ```

        ## Import

        `aws_datasync_location_nfs` can be imported by using the DataSync Task Amazon Resource Name (ARN), e.g.

        ```sh
         $ pulumi import aws:datasync/nfsLocation:NfsLocation example arn:aws:datasync:us-east-1:123456789012:location/loc-12345678901234567
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['NfsLocationOnPremConfigArgs']] on_prem_config: Configuration block containing information for connecting to the NFS File System.
        :param pulumi.Input[str] server_hostname: Specifies the IP address or DNS name of the NFS server. The DataSync Agent(s) use this to mount the NFS server.
        :param pulumi.Input[str] subdirectory: Subdirectory to perform actions as source or destination. Should be exported by the NFS server.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value pairs of resource tags to assign to the DataSync Location. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider .
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: NfsLocationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages an NFS Location within AWS DataSync.

        > **NOTE:** The DataSync Agents must be available before creating this resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.datasync.NfsLocation("example",
            server_hostname="nfs.example.com",
            subdirectory="/exported/path",
            on_prem_config=aws.datasync.NfsLocationOnPremConfigArgs(
                agent_arns=[aws_datasync_agent["example"]["arn"]],
            ))
        ```

        ## Import

        `aws_datasync_location_nfs` can be imported by using the DataSync Task Amazon Resource Name (ARN), e.g.

        ```sh
         $ pulumi import aws:datasync/nfsLocation:NfsLocation example arn:aws:datasync:us-east-1:123456789012:location/loc-12345678901234567
        ```

        :param str resource_name: The name of the resource.
        :param NfsLocationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(NfsLocationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 on_prem_config: Optional[pulumi.Input[pulumi.InputType['NfsLocationOnPremConfigArgs']]] = None,
                 server_hostname: Optional[pulumi.Input[str]] = None,
                 subdirectory: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = NfsLocationArgs.__new__(NfsLocationArgs)

            if on_prem_config is None and not opts.urn:
                raise TypeError("Missing required property 'on_prem_config'")
            __props__.__dict__["on_prem_config"] = on_prem_config
            if server_hostname is None and not opts.urn:
                raise TypeError("Missing required property 'server_hostname'")
            __props__.__dict__["server_hostname"] = server_hostname
            if subdirectory is None and not opts.urn:
                raise TypeError("Missing required property 'subdirectory'")
            __props__.__dict__["subdirectory"] = subdirectory
            __props__.__dict__["tags"] = tags
            __props__.__dict__["tags_all"] = tags_all
            __props__.__dict__["arn"] = None
            __props__.__dict__["uri"] = None
        super(NfsLocation, __self__).__init__(
            'aws:datasync/nfsLocation:NfsLocation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            on_prem_config: Optional[pulumi.Input[pulumi.InputType['NfsLocationOnPremConfigArgs']]] = None,
            server_hostname: Optional[pulumi.Input[str]] = None,
            subdirectory: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            uri: Optional[pulumi.Input[str]] = None) -> 'NfsLocation':
        """
        Get an existing NfsLocation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: Amazon Resource Name (ARN) of the DataSync Location.
        :param pulumi.Input[pulumi.InputType['NfsLocationOnPremConfigArgs']] on_prem_config: Configuration block containing information for connecting to the NFS File System.
        :param pulumi.Input[str] server_hostname: Specifies the IP address or DNS name of the NFS server. The DataSync Agent(s) use this to mount the NFS server.
        :param pulumi.Input[str] subdirectory: Subdirectory to perform actions as source or destination. Should be exported by the NFS server.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value pairs of resource tags to assign to the DataSync Location. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider .
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _NfsLocationState.__new__(_NfsLocationState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["on_prem_config"] = on_prem_config
        __props__.__dict__["server_hostname"] = server_hostname
        __props__.__dict__["subdirectory"] = subdirectory
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        __props__.__dict__["uri"] = uri
        return NfsLocation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        Amazon Resource Name (ARN) of the DataSync Location.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="onPremConfig")
    def on_prem_config(self) -> pulumi.Output['outputs.NfsLocationOnPremConfig']:
        """
        Configuration block containing information for connecting to the NFS File System.
        """
        return pulumi.get(self, "on_prem_config")

    @property
    @pulumi.getter(name="serverHostname")
    def server_hostname(self) -> pulumi.Output[str]:
        """
        Specifies the IP address or DNS name of the NFS server. The DataSync Agent(s) use this to mount the NFS server.
        """
        return pulumi.get(self, "server_hostname")

    @property
    @pulumi.getter
    def subdirectory(self) -> pulumi.Output[str]:
        """
        Subdirectory to perform actions as source or destination. Should be exported by the NFS server.
        """
        return pulumi.get(self, "subdirectory")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Key-value pairs of resource tags to assign to the DataSync Location. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> pulumi.Output[Mapping[str, str]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider .
        """
        return pulumi.get(self, "tags_all")

    @property
    @pulumi.getter
    def uri(self) -> pulumi.Output[str]:
        return pulumi.get(self, "uri")

