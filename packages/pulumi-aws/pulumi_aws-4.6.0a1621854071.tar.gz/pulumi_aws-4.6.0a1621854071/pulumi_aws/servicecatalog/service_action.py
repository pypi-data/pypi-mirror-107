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

__all__ = ['ServiceActionArgs', 'ServiceAction']

@pulumi.input_type
class ServiceActionArgs:
    def __init__(__self__, *,
                 definition: pulumi.Input['ServiceActionDefinitionArgs'],
                 accept_language: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ServiceAction resource.
        :param pulumi.Input['ServiceActionDefinitionArgs'] definition: Self-service action definition configuration block. Detailed below.
        :param pulumi.Input[str] accept_language: Language code. Valid values are `en` (English), `jp` (Japanese), and `zh` (Chinese). Default is `en`.
        :param pulumi.Input[str] description: Self-service action description.
        :param pulumi.Input[str] name: Self-service action name.
        """
        pulumi.set(__self__, "definition", definition)
        if accept_language is not None:
            pulumi.set(__self__, "accept_language", accept_language)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def definition(self) -> pulumi.Input['ServiceActionDefinitionArgs']:
        """
        Self-service action definition configuration block. Detailed below.
        """
        return pulumi.get(self, "definition")

    @definition.setter
    def definition(self, value: pulumi.Input['ServiceActionDefinitionArgs']):
        pulumi.set(self, "definition", value)

    @property
    @pulumi.getter(name="acceptLanguage")
    def accept_language(self) -> Optional[pulumi.Input[str]]:
        """
        Language code. Valid values are `en` (English), `jp` (Japanese), and `zh` (Chinese). Default is `en`.
        """
        return pulumi.get(self, "accept_language")

    @accept_language.setter
    def accept_language(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "accept_language", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Self-service action description.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Self-service action name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _ServiceActionState:
    def __init__(__self__, *,
                 accept_language: Optional[pulumi.Input[str]] = None,
                 definition: Optional[pulumi.Input['ServiceActionDefinitionArgs']] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ServiceAction resources.
        :param pulumi.Input[str] accept_language: Language code. Valid values are `en` (English), `jp` (Japanese), and `zh` (Chinese). Default is `en`.
        :param pulumi.Input['ServiceActionDefinitionArgs'] definition: Self-service action definition configuration block. Detailed below.
        :param pulumi.Input[str] description: Self-service action description.
        :param pulumi.Input[str] name: Self-service action name.
        """
        if accept_language is not None:
            pulumi.set(__self__, "accept_language", accept_language)
        if definition is not None:
            pulumi.set(__self__, "definition", definition)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="acceptLanguage")
    def accept_language(self) -> Optional[pulumi.Input[str]]:
        """
        Language code. Valid values are `en` (English), `jp` (Japanese), and `zh` (Chinese). Default is `en`.
        """
        return pulumi.get(self, "accept_language")

    @accept_language.setter
    def accept_language(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "accept_language", value)

    @property
    @pulumi.getter
    def definition(self) -> Optional[pulumi.Input['ServiceActionDefinitionArgs']]:
        """
        Self-service action definition configuration block. Detailed below.
        """
        return pulumi.get(self, "definition")

    @definition.setter
    def definition(self, value: Optional[pulumi.Input['ServiceActionDefinitionArgs']]):
        pulumi.set(self, "definition", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Self-service action description.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Self-service action name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


class ServiceAction(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 accept_language: Optional[pulumi.Input[str]] = None,
                 definition: Optional[pulumi.Input[pulumi.InputType['ServiceActionDefinitionArgs']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a Service Catalog self-service action.

        ## Example Usage
        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.servicecatalog.ServiceAction("example",
            definition=aws.servicecatalog.ServiceActionDefinitionArgs(
                name="AWS-RestartEC2Instance",
            ),
            description="Motor generator unit")
        ```

        ## Import

        `aws_servicecatalog_service_action` can be imported using the service action ID, e.g.

        ```sh
         $ pulumi import aws:servicecatalog/serviceAction:ServiceAction example act-f1w12eperfslh
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] accept_language: Language code. Valid values are `en` (English), `jp` (Japanese), and `zh` (Chinese). Default is `en`.
        :param pulumi.Input[pulumi.InputType['ServiceActionDefinitionArgs']] definition: Self-service action definition configuration block. Detailed below.
        :param pulumi.Input[str] description: Self-service action description.
        :param pulumi.Input[str] name: Self-service action name.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ServiceActionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Service Catalog self-service action.

        ## Example Usage
        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.servicecatalog.ServiceAction("example",
            definition=aws.servicecatalog.ServiceActionDefinitionArgs(
                name="AWS-RestartEC2Instance",
            ),
            description="Motor generator unit")
        ```

        ## Import

        `aws_servicecatalog_service_action` can be imported using the service action ID, e.g.

        ```sh
         $ pulumi import aws:servicecatalog/serviceAction:ServiceAction example act-f1w12eperfslh
        ```

        :param str resource_name: The name of the resource.
        :param ServiceActionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ServiceActionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 accept_language: Optional[pulumi.Input[str]] = None,
                 definition: Optional[pulumi.Input[pulumi.InputType['ServiceActionDefinitionArgs']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
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
            __props__ = ServiceActionArgs.__new__(ServiceActionArgs)

            __props__.__dict__["accept_language"] = accept_language
            if definition is None and not opts.urn:
                raise TypeError("Missing required property 'definition'")
            __props__.__dict__["definition"] = definition
            __props__.__dict__["description"] = description
            __props__.__dict__["name"] = name
        super(ServiceAction, __self__).__init__(
            'aws:servicecatalog/serviceAction:ServiceAction',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            accept_language: Optional[pulumi.Input[str]] = None,
            definition: Optional[pulumi.Input[pulumi.InputType['ServiceActionDefinitionArgs']]] = None,
            description: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None) -> 'ServiceAction':
        """
        Get an existing ServiceAction resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] accept_language: Language code. Valid values are `en` (English), `jp` (Japanese), and `zh` (Chinese). Default is `en`.
        :param pulumi.Input[pulumi.InputType['ServiceActionDefinitionArgs']] definition: Self-service action definition configuration block. Detailed below.
        :param pulumi.Input[str] description: Self-service action description.
        :param pulumi.Input[str] name: Self-service action name.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ServiceActionState.__new__(_ServiceActionState)

        __props__.__dict__["accept_language"] = accept_language
        __props__.__dict__["definition"] = definition
        __props__.__dict__["description"] = description
        __props__.__dict__["name"] = name
        return ServiceAction(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="acceptLanguage")
    def accept_language(self) -> pulumi.Output[Optional[str]]:
        """
        Language code. Valid values are `en` (English), `jp` (Japanese), and `zh` (Chinese). Default is `en`.
        """
        return pulumi.get(self, "accept_language")

    @property
    @pulumi.getter
    def definition(self) -> pulumi.Output['outputs.ServiceActionDefinition']:
        """
        Self-service action definition configuration block. Detailed below.
        """
        return pulumi.get(self, "definition")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[str]:
        """
        Self-service action description.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Self-service action name.
        """
        return pulumi.get(self, "name")

