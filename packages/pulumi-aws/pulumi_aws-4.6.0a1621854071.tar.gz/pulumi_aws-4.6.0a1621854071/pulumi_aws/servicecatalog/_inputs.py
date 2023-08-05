# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'ProductProvisioningArtifactParametersArgs',
    'ServiceActionDefinitionArgs',
]

@pulumi.input_type
class ProductProvisioningArtifactParametersArgs:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 disable_template_validation: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 template_physical_id: Optional[pulumi.Input[str]] = None,
                 template_url: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] description: Description of the provisioning artifact (i.e., version), including how it differs from the previous provisioning artifact.
        :param pulumi.Input[bool] disable_template_validation: Whether AWS Service Catalog stops validating the specified provisioning artifact template even if it is invalid.
        :param pulumi.Input[str] name: Name of the provisioning artifact (for example, `v1`, `v2beta`). No spaces are allowed.
        :param pulumi.Input[str] template_physical_id: Template source as the physical ID of the resource that contains the template. Currently only supports CloudFormation stack ARN. Specify the physical ID as `arn:[partition]:cloudformation:[region]:[account ID]:stack/[stack name]/[resource ID]`.
        :param pulumi.Input[str] template_url: Template source as URL of the CloudFormation template in Amazon S3.
        :param pulumi.Input[str] type: Type of provisioning artifact. Valid values: `CLOUD_FORMATION_TEMPLATE`, `MARKETPLACE_AMI`, `MARKETPLACE_CAR` (Marketplace Clusters and AWS Resources).
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if disable_template_validation is not None:
            pulumi.set(__self__, "disable_template_validation", disable_template_validation)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if template_physical_id is not None:
            pulumi.set(__self__, "template_physical_id", template_physical_id)
        if template_url is not None:
            pulumi.set(__self__, "template_url", template_url)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the provisioning artifact (i.e., version), including how it differs from the previous provisioning artifact.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="disableTemplateValidation")
    def disable_template_validation(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether AWS Service Catalog stops validating the specified provisioning artifact template even if it is invalid.
        """
        return pulumi.get(self, "disable_template_validation")

    @disable_template_validation.setter
    def disable_template_validation(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "disable_template_validation", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the provisioning artifact (for example, `v1`, `v2beta`). No spaces are allowed.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="templatePhysicalId")
    def template_physical_id(self) -> Optional[pulumi.Input[str]]:
        """
        Template source as the physical ID of the resource that contains the template. Currently only supports CloudFormation stack ARN. Specify the physical ID as `arn:[partition]:cloudformation:[region]:[account ID]:stack/[stack name]/[resource ID]`.
        """
        return pulumi.get(self, "template_physical_id")

    @template_physical_id.setter
    def template_physical_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "template_physical_id", value)

    @property
    @pulumi.getter(name="templateUrl")
    def template_url(self) -> Optional[pulumi.Input[str]]:
        """
        Template source as URL of the CloudFormation template in Amazon S3.
        """
        return pulumi.get(self, "template_url")

    @template_url.setter
    def template_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "template_url", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Type of provisioning artifact. Valid values: `CLOUD_FORMATION_TEMPLATE`, `MARKETPLACE_AMI`, `MARKETPLACE_CAR` (Marketplace Clusters and AWS Resources).
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)


@pulumi.input_type
class ServiceActionDefinitionArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 version: pulumi.Input[str],
                 assume_role: Optional[pulumi.Input[str]] = None,
                 parameters: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] name: Name of the SSM document. For example, `AWS-RestartEC2Instance`. If you are using a shared SSM document, you must provide the ARN instead of the name.
        :param pulumi.Input[str] version: SSM document version. For example, `1`.
        :param pulumi.Input[str] assume_role: ARN of the role that performs the self-service actions on your behalf. For example, `arn:aws:iam::12345678910:role/ActionRole`. To reuse the provisioned product launch role, set to `LAUNCH_ROLE`.
        :param pulumi.Input[str] parameters: List of parameters in JSON format. For example: `[{\"Name\":\"InstanceId\",\"Type\":\"TARGET\"}]` or `[{\"Name\":\"InstanceId\",\"Type\":\"TEXT_VALUE\"}]`.
        :param pulumi.Input[str] type: Service action definition type. Valid value is `SSM_AUTOMATION`. Default is `SSM_AUTOMATION`.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "version", version)
        if assume_role is not None:
            pulumi.set(__self__, "assume_role", assume_role)
        if parameters is not None:
            pulumi.set(__self__, "parameters", parameters)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Name of the SSM document. For example, `AWS-RestartEC2Instance`. If you are using a shared SSM document, you must provide the ARN instead of the name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def version(self) -> pulumi.Input[str]:
        """
        SSM document version. For example, `1`.
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: pulumi.Input[str]):
        pulumi.set(self, "version", value)

    @property
    @pulumi.getter(name="assumeRole")
    def assume_role(self) -> Optional[pulumi.Input[str]]:
        """
        ARN of the role that performs the self-service actions on your behalf. For example, `arn:aws:iam::12345678910:role/ActionRole`. To reuse the provisioned product launch role, set to `LAUNCH_ROLE`.
        """
        return pulumi.get(self, "assume_role")

    @assume_role.setter
    def assume_role(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "assume_role", value)

    @property
    @pulumi.getter
    def parameters(self) -> Optional[pulumi.Input[str]]:
        """
        List of parameters in JSON format. For example: `[{\"Name\":\"InstanceId\",\"Type\":\"TARGET\"}]` or `[{\"Name\":\"InstanceId\",\"Type\":\"TEXT_VALUE\"}]`.
        """
        return pulumi.get(self, "parameters")

    @parameters.setter
    def parameters(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "parameters", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Service action definition type. Valid value is `SSM_AUTOMATION`. Default is `SSM_AUTOMATION`.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)


