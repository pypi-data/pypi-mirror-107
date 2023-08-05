# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['SpotDatafeedSubscriptionArgs', 'SpotDatafeedSubscription']

@pulumi.input_type
class SpotDatafeedSubscriptionArgs:
    def __init__(__self__, *,
                 bucket: pulumi.Input[str],
                 prefix: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a SpotDatafeedSubscription resource.
        :param pulumi.Input[str] bucket: The Amazon S3 bucket in which to store the Spot instance data feed.
        :param pulumi.Input[str] prefix: Path of folder inside bucket to place spot pricing data.
        """
        pulumi.set(__self__, "bucket", bucket)
        if prefix is not None:
            pulumi.set(__self__, "prefix", prefix)

    @property
    @pulumi.getter
    def bucket(self) -> pulumi.Input[str]:
        """
        The Amazon S3 bucket in which to store the Spot instance data feed.
        """
        return pulumi.get(self, "bucket")

    @bucket.setter
    def bucket(self, value: pulumi.Input[str]):
        pulumi.set(self, "bucket", value)

    @property
    @pulumi.getter
    def prefix(self) -> Optional[pulumi.Input[str]]:
        """
        Path of folder inside bucket to place spot pricing data.
        """
        return pulumi.get(self, "prefix")

    @prefix.setter
    def prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "prefix", value)


@pulumi.input_type
class _SpotDatafeedSubscriptionState:
    def __init__(__self__, *,
                 bucket: Optional[pulumi.Input[str]] = None,
                 prefix: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering SpotDatafeedSubscription resources.
        :param pulumi.Input[str] bucket: The Amazon S3 bucket in which to store the Spot instance data feed.
        :param pulumi.Input[str] prefix: Path of folder inside bucket to place spot pricing data.
        """
        if bucket is not None:
            pulumi.set(__self__, "bucket", bucket)
        if prefix is not None:
            pulumi.set(__self__, "prefix", prefix)

    @property
    @pulumi.getter
    def bucket(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon S3 bucket in which to store the Spot instance data feed.
        """
        return pulumi.get(self, "bucket")

    @bucket.setter
    def bucket(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bucket", value)

    @property
    @pulumi.getter
    def prefix(self) -> Optional[pulumi.Input[str]]:
        """
        Path of folder inside bucket to place spot pricing data.
        """
        return pulumi.get(self, "prefix")

    @prefix.setter
    def prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "prefix", value)


class SpotDatafeedSubscription(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bucket: Optional[pulumi.Input[str]] = None,
                 prefix: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        > **Note:** There is only a single subscription allowed per account.

        To help you understand the charges for your Spot instances, Amazon EC2 provides a data feed that describes your Spot instance usage and pricing.
        This data feed is sent to an Amazon S3 bucket that you specify when you subscribe to the data feed.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        default_bucket = aws.s3.Bucket("defaultBucket")
        default_spot_datafeed_subscription = aws.ec2.SpotDatafeedSubscription("defaultSpotDatafeedSubscription",
            bucket=default_bucket.bucket,
            prefix="my_subdirectory")
        ```

        ## Import

        A Spot Datafeed Subscription can be imported using the word `spot-datafeed-subscription`, e.g.

        ```sh
         $ pulumi import aws:ec2/spotDatafeedSubscription:SpotDatafeedSubscription mysubscription spot-datafeed-subscription
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bucket: The Amazon S3 bucket in which to store the Spot instance data feed.
        :param pulumi.Input[str] prefix: Path of folder inside bucket to place spot pricing data.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SpotDatafeedSubscriptionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        > **Note:** There is only a single subscription allowed per account.

        To help you understand the charges for your Spot instances, Amazon EC2 provides a data feed that describes your Spot instance usage and pricing.
        This data feed is sent to an Amazon S3 bucket that you specify when you subscribe to the data feed.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        default_bucket = aws.s3.Bucket("defaultBucket")
        default_spot_datafeed_subscription = aws.ec2.SpotDatafeedSubscription("defaultSpotDatafeedSubscription",
            bucket=default_bucket.bucket,
            prefix="my_subdirectory")
        ```

        ## Import

        A Spot Datafeed Subscription can be imported using the word `spot-datafeed-subscription`, e.g.

        ```sh
         $ pulumi import aws:ec2/spotDatafeedSubscription:SpotDatafeedSubscription mysubscription spot-datafeed-subscription
        ```

        :param str resource_name: The name of the resource.
        :param SpotDatafeedSubscriptionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SpotDatafeedSubscriptionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bucket: Optional[pulumi.Input[str]] = None,
                 prefix: Optional[pulumi.Input[str]] = None,
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
            __props__ = SpotDatafeedSubscriptionArgs.__new__(SpotDatafeedSubscriptionArgs)

            if bucket is None and not opts.urn:
                raise TypeError("Missing required property 'bucket'")
            __props__.__dict__["bucket"] = bucket
            __props__.__dict__["prefix"] = prefix
        super(SpotDatafeedSubscription, __self__).__init__(
            'aws:ec2/spotDatafeedSubscription:SpotDatafeedSubscription',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            bucket: Optional[pulumi.Input[str]] = None,
            prefix: Optional[pulumi.Input[str]] = None) -> 'SpotDatafeedSubscription':
        """
        Get an existing SpotDatafeedSubscription resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bucket: The Amazon S3 bucket in which to store the Spot instance data feed.
        :param pulumi.Input[str] prefix: Path of folder inside bucket to place spot pricing data.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _SpotDatafeedSubscriptionState.__new__(_SpotDatafeedSubscriptionState)

        __props__.__dict__["bucket"] = bucket
        __props__.__dict__["prefix"] = prefix
        return SpotDatafeedSubscription(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def bucket(self) -> pulumi.Output[str]:
        """
        The Amazon S3 bucket in which to store the Spot instance data feed.
        """
        return pulumi.get(self, "bucket")

    @property
    @pulumi.getter
    def prefix(self) -> pulumi.Output[Optional[str]]:
        """
        Path of folder inside bucket to place spot pricing data.
        """
        return pulumi.get(self, "prefix")

