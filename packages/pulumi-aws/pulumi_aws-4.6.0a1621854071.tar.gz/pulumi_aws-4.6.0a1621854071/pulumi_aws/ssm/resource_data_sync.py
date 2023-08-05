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

__all__ = ['ResourceDataSyncArgs', 'ResourceDataSync']

@pulumi.input_type
class ResourceDataSyncArgs:
    def __init__(__self__, *,
                 s3_destination: pulumi.Input['ResourceDataSyncS3DestinationArgs'],
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ResourceDataSync resource.
        :param pulumi.Input['ResourceDataSyncS3DestinationArgs'] s3_destination: Amazon S3 configuration details for the sync.
        :param pulumi.Input[str] name: Name for the configuration.
        """
        pulumi.set(__self__, "s3_destination", s3_destination)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="s3Destination")
    def s3_destination(self) -> pulumi.Input['ResourceDataSyncS3DestinationArgs']:
        """
        Amazon S3 configuration details for the sync.
        """
        return pulumi.get(self, "s3_destination")

    @s3_destination.setter
    def s3_destination(self, value: pulumi.Input['ResourceDataSyncS3DestinationArgs']):
        pulumi.set(self, "s3_destination", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name for the configuration.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _ResourceDataSyncState:
    def __init__(__self__, *,
                 name: Optional[pulumi.Input[str]] = None,
                 s3_destination: Optional[pulumi.Input['ResourceDataSyncS3DestinationArgs']] = None):
        """
        Input properties used for looking up and filtering ResourceDataSync resources.
        :param pulumi.Input[str] name: Name for the configuration.
        :param pulumi.Input['ResourceDataSyncS3DestinationArgs'] s3_destination: Amazon S3 configuration details for the sync.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if s3_destination is not None:
            pulumi.set(__self__, "s3_destination", s3_destination)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name for the configuration.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="s3Destination")
    def s3_destination(self) -> Optional[pulumi.Input['ResourceDataSyncS3DestinationArgs']]:
        """
        Amazon S3 configuration details for the sync.
        """
        return pulumi.get(self, "s3_destination")

    @s3_destination.setter
    def s3_destination(self, value: Optional[pulumi.Input['ResourceDataSyncS3DestinationArgs']]):
        pulumi.set(self, "s3_destination", value)


class ResourceDataSync(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 s3_destination: Optional[pulumi.Input[pulumi.InputType['ResourceDataSyncS3DestinationArgs']]] = None,
                 __props__=None):
        """
        Provides a SSM resource data sync.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        hoge_bucket = aws.s3.Bucket("hogeBucket")
        hoge_bucket_policy = aws.s3.BucketPolicy("hogeBucketPolicy",
            bucket=hoge_bucket.bucket,
            policy=\"\"\"{
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "SSMBucketPermissionsCheck",
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "ssm.amazonaws.com"
                    },
                    "Action": "s3:GetBucketAcl",
                    "Resource": "arn:aws:s3:::tf-test-bucket-1234"
                },
                {
                    "Sid": " SSMBucketDelivery",
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "ssm.amazonaws.com"
                    },
                    "Action": "s3:PutObject",
                    "Resource": ["arn:aws:s3:::tf-test-bucket-1234/*"],
                    "Condition": {
                        "StringEquals": {
                            "s3:x-amz-acl": "bucket-owner-full-control"
                        }
                    }
                }
            ]
        }
        \"\"\")
        foo = aws.ssm.ResourceDataSync("foo", s3_destination=aws.ssm.ResourceDataSyncS3DestinationArgs(
            bucket_name=hoge_bucket.bucket,
            region=hoge_bucket.region,
        ))
        ```

        ## Import

        SSM resource data sync can be imported using the `name`, e.g.

        ```sh
         $ pulumi import aws:ssm/resourceDataSync:ResourceDataSync example example-name
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: Name for the configuration.
        :param pulumi.Input[pulumi.InputType['ResourceDataSyncS3DestinationArgs']] s3_destination: Amazon S3 configuration details for the sync.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ResourceDataSyncArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a SSM resource data sync.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        hoge_bucket = aws.s3.Bucket("hogeBucket")
        hoge_bucket_policy = aws.s3.BucketPolicy("hogeBucketPolicy",
            bucket=hoge_bucket.bucket,
            policy=\"\"\"{
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "SSMBucketPermissionsCheck",
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "ssm.amazonaws.com"
                    },
                    "Action": "s3:GetBucketAcl",
                    "Resource": "arn:aws:s3:::tf-test-bucket-1234"
                },
                {
                    "Sid": " SSMBucketDelivery",
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "ssm.amazonaws.com"
                    },
                    "Action": "s3:PutObject",
                    "Resource": ["arn:aws:s3:::tf-test-bucket-1234/*"],
                    "Condition": {
                        "StringEquals": {
                            "s3:x-amz-acl": "bucket-owner-full-control"
                        }
                    }
                }
            ]
        }
        \"\"\")
        foo = aws.ssm.ResourceDataSync("foo", s3_destination=aws.ssm.ResourceDataSyncS3DestinationArgs(
            bucket_name=hoge_bucket.bucket,
            region=hoge_bucket.region,
        ))
        ```

        ## Import

        SSM resource data sync can be imported using the `name`, e.g.

        ```sh
         $ pulumi import aws:ssm/resourceDataSync:ResourceDataSync example example-name
        ```

        :param str resource_name: The name of the resource.
        :param ResourceDataSyncArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ResourceDataSyncArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 s3_destination: Optional[pulumi.Input[pulumi.InputType['ResourceDataSyncS3DestinationArgs']]] = None,
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
            __props__ = ResourceDataSyncArgs.__new__(ResourceDataSyncArgs)

            __props__.__dict__["name"] = name
            if s3_destination is None and not opts.urn:
                raise TypeError("Missing required property 's3_destination'")
            __props__.__dict__["s3_destination"] = s3_destination
        super(ResourceDataSync, __self__).__init__(
            'aws:ssm/resourceDataSync:ResourceDataSync',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            name: Optional[pulumi.Input[str]] = None,
            s3_destination: Optional[pulumi.Input[pulumi.InputType['ResourceDataSyncS3DestinationArgs']]] = None) -> 'ResourceDataSync':
        """
        Get an existing ResourceDataSync resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: Name for the configuration.
        :param pulumi.Input[pulumi.InputType['ResourceDataSyncS3DestinationArgs']] s3_destination: Amazon S3 configuration details for the sync.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ResourceDataSyncState.__new__(_ResourceDataSyncState)

        __props__.__dict__["name"] = name
        __props__.__dict__["s3_destination"] = s3_destination
        return ResourceDataSync(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name for the configuration.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="s3Destination")
    def s3_destination(self) -> pulumi.Output['outputs.ResourceDataSyncS3Destination']:
        """
        Amazon S3 configuration details for the sync.
        """
        return pulumi.get(self, "s3_destination")

