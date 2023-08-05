# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'ConfigurationAggregatorAccountAggregationSourceArgs',
    'ConfigurationAggregatorOrganizationAggregationSourceArgs',
    'ConformancePackInputParameterArgs',
    'DeliveryChannelSnapshotDeliveryPropertiesArgs',
    'RecorderRecordingGroupArgs',
    'RemediationConfigurationParameterArgs',
    'RuleScopeArgs',
    'RuleSourceArgs',
    'RuleSourceSourceDetailArgs',
]

@pulumi.input_type
class ConfigurationAggregatorAccountAggregationSourceArgs:
    def __init__(__self__, *,
                 account_ids: pulumi.Input[Sequence[pulumi.Input[str]]],
                 all_regions: Optional[pulumi.Input[bool]] = None,
                 regions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[Sequence[pulumi.Input[str]]] account_ids: List of 12-digit account IDs of the account(s) being aggregated.
        :param pulumi.Input[bool] all_regions: If true, aggregate existing AWS Config regions and future regions.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] regions: List of source regions being aggregated.
        """
        pulumi.set(__self__, "account_ids", account_ids)
        if all_regions is not None:
            pulumi.set(__self__, "all_regions", all_regions)
        if regions is not None:
            pulumi.set(__self__, "regions", regions)

    @property
    @pulumi.getter(name="accountIds")
    def account_ids(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        List of 12-digit account IDs of the account(s) being aggregated.
        """
        return pulumi.get(self, "account_ids")

    @account_ids.setter
    def account_ids(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "account_ids", value)

    @property
    @pulumi.getter(name="allRegions")
    def all_regions(self) -> Optional[pulumi.Input[bool]]:
        """
        If true, aggregate existing AWS Config regions and future regions.
        """
        return pulumi.get(self, "all_regions")

    @all_regions.setter
    def all_regions(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "all_regions", value)

    @property
    @pulumi.getter
    def regions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of source regions being aggregated.
        """
        return pulumi.get(self, "regions")

    @regions.setter
    def regions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "regions", value)


@pulumi.input_type
class ConfigurationAggregatorOrganizationAggregationSourceArgs:
    def __init__(__self__, *,
                 role_arn: pulumi.Input[str],
                 all_regions: Optional[pulumi.Input[bool]] = None,
                 regions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[str] role_arn: ARN of the IAM role used to retrieve AWS Organization details associated with the aggregator account.
        :param pulumi.Input[bool] all_regions: If true, aggregate existing AWS Config regions and future regions.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] regions: List of source regions being aggregated.
        """
        pulumi.set(__self__, "role_arn", role_arn)
        if all_regions is not None:
            pulumi.set(__self__, "all_regions", all_regions)
        if regions is not None:
            pulumi.set(__self__, "regions", regions)

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> pulumi.Input[str]:
        """
        ARN of the IAM role used to retrieve AWS Organization details associated with the aggregator account.
        """
        return pulumi.get(self, "role_arn")

    @role_arn.setter
    def role_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "role_arn", value)

    @property
    @pulumi.getter(name="allRegions")
    def all_regions(self) -> Optional[pulumi.Input[bool]]:
        """
        If true, aggregate existing AWS Config regions and future regions.
        """
        return pulumi.get(self, "all_regions")

    @all_regions.setter
    def all_regions(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "all_regions", value)

    @property
    @pulumi.getter
    def regions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of source regions being aggregated.
        """
        return pulumi.get(self, "regions")

    @regions.setter
    def regions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "regions", value)


@pulumi.input_type
class ConformancePackInputParameterArgs:
    def __init__(__self__, *,
                 parameter_name: pulumi.Input[str],
                 parameter_value: pulumi.Input[str]):
        """
        :param pulumi.Input[str] parameter_name: The input key.
        :param pulumi.Input[str] parameter_value: The input value.
        """
        pulumi.set(__self__, "parameter_name", parameter_name)
        pulumi.set(__self__, "parameter_value", parameter_value)

    @property
    @pulumi.getter(name="parameterName")
    def parameter_name(self) -> pulumi.Input[str]:
        """
        The input key.
        """
        return pulumi.get(self, "parameter_name")

    @parameter_name.setter
    def parameter_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "parameter_name", value)

    @property
    @pulumi.getter(name="parameterValue")
    def parameter_value(self) -> pulumi.Input[str]:
        """
        The input value.
        """
        return pulumi.get(self, "parameter_value")

    @parameter_value.setter
    def parameter_value(self, value: pulumi.Input[str]):
        pulumi.set(self, "parameter_value", value)


@pulumi.input_type
class DeliveryChannelSnapshotDeliveryPropertiesArgs:
    def __init__(__self__, *,
                 delivery_frequency: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] delivery_frequency: - The frequency with which AWS Config recurringly delivers configuration snapshots. e.g. `One_Hour` or `Three_Hours`. Valid values are listed [here](https://docs.aws.amazon.com/config/latest/APIReference/API_ConfigSnapshotDeliveryProperties.html#API_ConfigSnapshotDeliveryProperties_Contents).
        """
        if delivery_frequency is not None:
            pulumi.set(__self__, "delivery_frequency", delivery_frequency)

    @property
    @pulumi.getter(name="deliveryFrequency")
    def delivery_frequency(self) -> Optional[pulumi.Input[str]]:
        """
        - The frequency with which AWS Config recurringly delivers configuration snapshots. e.g. `One_Hour` or `Three_Hours`. Valid values are listed [here](https://docs.aws.amazon.com/config/latest/APIReference/API_ConfigSnapshotDeliveryProperties.html#API_ConfigSnapshotDeliveryProperties_Contents).
        """
        return pulumi.get(self, "delivery_frequency")

    @delivery_frequency.setter
    def delivery_frequency(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "delivery_frequency", value)


@pulumi.input_type
class RecorderRecordingGroupArgs:
    def __init__(__self__, *,
                 all_supported: Optional[pulumi.Input[bool]] = None,
                 include_global_resource_types: Optional[pulumi.Input[bool]] = None,
                 resource_types: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[bool] all_supported: Specifies whether AWS Config records configuration changes for every supported type of regional resource (which includes any new type that will become supported in the future). Conflicts with `resource_types`. Defaults to `true`.
        :param pulumi.Input[bool] include_global_resource_types: Specifies whether AWS Config includes all supported types of *global resources* with the resources that it records. Requires `all_supported = true`. Conflicts with `resource_types`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] resource_types: A list that specifies the types of AWS resources for which AWS Config records configuration changes (for example, `AWS::EC2::Instance` or `AWS::CloudTrail::Trail`). See [relevant part of AWS Docs](http://docs.aws.amazon.com/config/latest/APIReference/API_ResourceIdentifier.html#config-Type-ResourceIdentifier-resourceType) for available types. In order to use this attribute, `all_supported` must be set to false.
        """
        if all_supported is not None:
            pulumi.set(__self__, "all_supported", all_supported)
        if include_global_resource_types is not None:
            pulumi.set(__self__, "include_global_resource_types", include_global_resource_types)
        if resource_types is not None:
            pulumi.set(__self__, "resource_types", resource_types)

    @property
    @pulumi.getter(name="allSupported")
    def all_supported(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether AWS Config records configuration changes for every supported type of regional resource (which includes any new type that will become supported in the future). Conflicts with `resource_types`. Defaults to `true`.
        """
        return pulumi.get(self, "all_supported")

    @all_supported.setter
    def all_supported(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "all_supported", value)

    @property
    @pulumi.getter(name="includeGlobalResourceTypes")
    def include_global_resource_types(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether AWS Config includes all supported types of *global resources* with the resources that it records. Requires `all_supported = true`. Conflicts with `resource_types`.
        """
        return pulumi.get(self, "include_global_resource_types")

    @include_global_resource_types.setter
    def include_global_resource_types(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "include_global_resource_types", value)

    @property
    @pulumi.getter(name="resourceTypes")
    def resource_types(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list that specifies the types of AWS resources for which AWS Config records configuration changes (for example, `AWS::EC2::Instance` or `AWS::CloudTrail::Trail`). See [relevant part of AWS Docs](http://docs.aws.amazon.com/config/latest/APIReference/API_ResourceIdentifier.html#config-Type-ResourceIdentifier-resourceType) for available types. In order to use this attribute, `all_supported` must be set to false.
        """
        return pulumi.get(self, "resource_types")

    @resource_types.setter
    def resource_types(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "resource_types", value)


@pulumi.input_type
class RemediationConfigurationParameterArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 resource_value: Optional[pulumi.Input[str]] = None,
                 static_value: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] name: The name of the attribute.
        :param pulumi.Input[str] resource_value: The value is dynamic and changes at run-time.
        :param pulumi.Input[str] static_value: The value is static and does not change at run-time.
        """
        pulumi.set(__self__, "name", name)
        if resource_value is not None:
            pulumi.set(__self__, "resource_value", resource_value)
        if static_value is not None:
            pulumi.set(__self__, "static_value", static_value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the attribute.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="resourceValue")
    def resource_value(self) -> Optional[pulumi.Input[str]]:
        """
        The value is dynamic and changes at run-time.
        """
        return pulumi.get(self, "resource_value")

    @resource_value.setter
    def resource_value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_value", value)

    @property
    @pulumi.getter(name="staticValue")
    def static_value(self) -> Optional[pulumi.Input[str]]:
        """
        The value is static and does not change at run-time.
        """
        return pulumi.get(self, "static_value")

    @static_value.setter
    def static_value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "static_value", value)


@pulumi.input_type
class RuleScopeArgs:
    def __init__(__self__, *,
                 compliance_resource_id: Optional[pulumi.Input[str]] = None,
                 compliance_resource_types: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tag_key: Optional[pulumi.Input[str]] = None,
                 tag_value: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] compliance_resource_id: The IDs of the only AWS resource that you want to trigger an evaluation for the rule. If you specify a resource ID, you must specify one resource type for `compliance_resource_types`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] compliance_resource_types: A list of resource types of only those AWS resources that you want to trigger an evaluation for the rule. e.g. `AWS::EC2::Instance`. You can only specify one type if you also specify a resource ID for `compliance_resource_id`. See [relevant part of AWS Docs](http://docs.aws.amazon.com/config/latest/APIReference/API_ResourceIdentifier.html#config-Type-ResourceIdentifier-resourceType) for available types.
        :param pulumi.Input[str] tag_key: The tag key that is applied to only those AWS resources that you want you want to trigger an evaluation for the rule.
        :param pulumi.Input[str] tag_value: The tag value applied to only those AWS resources that you want to trigger an evaluation for the rule.
        """
        if compliance_resource_id is not None:
            pulumi.set(__self__, "compliance_resource_id", compliance_resource_id)
        if compliance_resource_types is not None:
            pulumi.set(__self__, "compliance_resource_types", compliance_resource_types)
        if tag_key is not None:
            pulumi.set(__self__, "tag_key", tag_key)
        if tag_value is not None:
            pulumi.set(__self__, "tag_value", tag_value)

    @property
    @pulumi.getter(name="complianceResourceId")
    def compliance_resource_id(self) -> Optional[pulumi.Input[str]]:
        """
        The IDs of the only AWS resource that you want to trigger an evaluation for the rule. If you specify a resource ID, you must specify one resource type for `compliance_resource_types`.
        """
        return pulumi.get(self, "compliance_resource_id")

    @compliance_resource_id.setter
    def compliance_resource_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "compliance_resource_id", value)

    @property
    @pulumi.getter(name="complianceResourceTypes")
    def compliance_resource_types(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of resource types of only those AWS resources that you want to trigger an evaluation for the rule. e.g. `AWS::EC2::Instance`. You can only specify one type if you also specify a resource ID for `compliance_resource_id`. See [relevant part of AWS Docs](http://docs.aws.amazon.com/config/latest/APIReference/API_ResourceIdentifier.html#config-Type-ResourceIdentifier-resourceType) for available types.
        """
        return pulumi.get(self, "compliance_resource_types")

    @compliance_resource_types.setter
    def compliance_resource_types(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "compliance_resource_types", value)

    @property
    @pulumi.getter(name="tagKey")
    def tag_key(self) -> Optional[pulumi.Input[str]]:
        """
        The tag key that is applied to only those AWS resources that you want you want to trigger an evaluation for the rule.
        """
        return pulumi.get(self, "tag_key")

    @tag_key.setter
    def tag_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "tag_key", value)

    @property
    @pulumi.getter(name="tagValue")
    def tag_value(self) -> Optional[pulumi.Input[str]]:
        """
        The tag value applied to only those AWS resources that you want to trigger an evaluation for the rule.
        """
        return pulumi.get(self, "tag_value")

    @tag_value.setter
    def tag_value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "tag_value", value)


@pulumi.input_type
class RuleSourceArgs:
    def __init__(__self__, *,
                 owner: pulumi.Input[str],
                 source_identifier: pulumi.Input[str],
                 source_details: Optional[pulumi.Input[Sequence[pulumi.Input['RuleSourceSourceDetailArgs']]]] = None):
        """
        :param pulumi.Input[str] owner: Indicates whether AWS or the customer owns and manages the AWS Config rule. Valid values are `AWS` or `CUSTOM_LAMBDA`. For more information about managed rules, see the [AWS Config Managed Rules documentation](https://docs.aws.amazon.com/config/latest/developerguide/evaluate-config_use-managed-rules.html). For more information about custom rules, see the [AWS Config Custom Rules documentation](https://docs.aws.amazon.com/config/latest/developerguide/evaluate-config_develop-rules.html). Custom Lambda Functions require permissions to allow the AWS Config service to invoke them, e.g. via the `lambda.Permission` resource.
        :param pulumi.Input[str] source_identifier: For AWS Config managed rules, a predefined identifier, e.g `IAM_PASSWORD_POLICY`. For custom Lambda rules, the identifier is the ARN of the Lambda Function, such as `arn:aws:lambda:us-east-1:123456789012:function:custom_rule_name` or the `arn` attribute of the `lambda.Function` resource.
        :param pulumi.Input[Sequence[pulumi.Input['RuleSourceSourceDetailArgs']]] source_details: Provides the source and type of the event that causes AWS Config to evaluate your AWS resources. Only valid if `owner` is `CUSTOM_LAMBDA`.
        """
        pulumi.set(__self__, "owner", owner)
        pulumi.set(__self__, "source_identifier", source_identifier)
        if source_details is not None:
            pulumi.set(__self__, "source_details", source_details)

    @property
    @pulumi.getter
    def owner(self) -> pulumi.Input[str]:
        """
        Indicates whether AWS or the customer owns and manages the AWS Config rule. Valid values are `AWS` or `CUSTOM_LAMBDA`. For more information about managed rules, see the [AWS Config Managed Rules documentation](https://docs.aws.amazon.com/config/latest/developerguide/evaluate-config_use-managed-rules.html). For more information about custom rules, see the [AWS Config Custom Rules documentation](https://docs.aws.amazon.com/config/latest/developerguide/evaluate-config_develop-rules.html). Custom Lambda Functions require permissions to allow the AWS Config service to invoke them, e.g. via the `lambda.Permission` resource.
        """
        return pulumi.get(self, "owner")

    @owner.setter
    def owner(self, value: pulumi.Input[str]):
        pulumi.set(self, "owner", value)

    @property
    @pulumi.getter(name="sourceIdentifier")
    def source_identifier(self) -> pulumi.Input[str]:
        """
        For AWS Config managed rules, a predefined identifier, e.g `IAM_PASSWORD_POLICY`. For custom Lambda rules, the identifier is the ARN of the Lambda Function, such as `arn:aws:lambda:us-east-1:123456789012:function:custom_rule_name` or the `arn` attribute of the `lambda.Function` resource.
        """
        return pulumi.get(self, "source_identifier")

    @source_identifier.setter
    def source_identifier(self, value: pulumi.Input[str]):
        pulumi.set(self, "source_identifier", value)

    @property
    @pulumi.getter(name="sourceDetails")
    def source_details(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['RuleSourceSourceDetailArgs']]]]:
        """
        Provides the source and type of the event that causes AWS Config to evaluate your AWS resources. Only valid if `owner` is `CUSTOM_LAMBDA`.
        """
        return pulumi.get(self, "source_details")

    @source_details.setter
    def source_details(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['RuleSourceSourceDetailArgs']]]]):
        pulumi.set(self, "source_details", value)


@pulumi.input_type
class RuleSourceSourceDetailArgs:
    def __init__(__self__, *,
                 event_source: Optional[pulumi.Input[str]] = None,
                 maximum_execution_frequency: Optional[pulumi.Input[str]] = None,
                 message_type: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] event_source: The source of the event, such as an AWS service, that triggers AWS Config to evaluate your AWS resources. This defaults to `aws.config` and is the only valid value.
        :param pulumi.Input[str] maximum_execution_frequency: The frequency that you want AWS Config to run evaluations for a rule that is triggered periodically. If specified, requires `message_type` to be `ScheduledNotification`.
        :param pulumi.Input[str] message_type: The type of notification that triggers AWS Config to run an evaluation for a rule. You can specify the following notification types:
        """
        if event_source is not None:
            pulumi.set(__self__, "event_source", event_source)
        if maximum_execution_frequency is not None:
            pulumi.set(__self__, "maximum_execution_frequency", maximum_execution_frequency)
        if message_type is not None:
            pulumi.set(__self__, "message_type", message_type)

    @property
    @pulumi.getter(name="eventSource")
    def event_source(self) -> Optional[pulumi.Input[str]]:
        """
        The source of the event, such as an AWS service, that triggers AWS Config to evaluate your AWS resources. This defaults to `aws.config` and is the only valid value.
        """
        return pulumi.get(self, "event_source")

    @event_source.setter
    def event_source(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "event_source", value)

    @property
    @pulumi.getter(name="maximumExecutionFrequency")
    def maximum_execution_frequency(self) -> Optional[pulumi.Input[str]]:
        """
        The frequency that you want AWS Config to run evaluations for a rule that is triggered periodically. If specified, requires `message_type` to be `ScheduledNotification`.
        """
        return pulumi.get(self, "maximum_execution_frequency")

    @maximum_execution_frequency.setter
    def maximum_execution_frequency(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "maximum_execution_frequency", value)

    @property
    @pulumi.getter(name="messageType")
    def message_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of notification that triggers AWS Config to run an evaluation for a rule. You can specify the following notification types:
        """
        return pulumi.get(self, "message_type")

    @message_type.setter
    def message_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "message_type", value)


