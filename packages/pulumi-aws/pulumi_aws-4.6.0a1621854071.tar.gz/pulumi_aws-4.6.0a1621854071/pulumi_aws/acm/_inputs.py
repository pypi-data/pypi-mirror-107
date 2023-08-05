# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'CertificateDomainValidationOptionArgs',
    'CertificateOptionsArgs',
]

@pulumi.input_type
class CertificateDomainValidationOptionArgs:
    def __init__(__self__, *,
                 domain_name: Optional[pulumi.Input[str]] = None,
                 resource_record_name: Optional[pulumi.Input[str]] = None,
                 resource_record_type: Optional[pulumi.Input[str]] = None,
                 resource_record_value: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] domain_name: A domain name for which the certificate should be issued
        :param pulumi.Input[str] resource_record_name: The name of the DNS record to create to validate the certificate
        :param pulumi.Input[str] resource_record_type: The type of DNS record to create
        :param pulumi.Input[str] resource_record_value: The value the DNS record needs to have
        """
        if domain_name is not None:
            pulumi.set(__self__, "domain_name", domain_name)
        if resource_record_name is not None:
            pulumi.set(__self__, "resource_record_name", resource_record_name)
        if resource_record_type is not None:
            pulumi.set(__self__, "resource_record_type", resource_record_type)
        if resource_record_value is not None:
            pulumi.set(__self__, "resource_record_value", resource_record_value)

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> Optional[pulumi.Input[str]]:
        """
        A domain name for which the certificate should be issued
        """
        return pulumi.get(self, "domain_name")

    @domain_name.setter
    def domain_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "domain_name", value)

    @property
    @pulumi.getter(name="resourceRecordName")
    def resource_record_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the DNS record to create to validate the certificate
        """
        return pulumi.get(self, "resource_record_name")

    @resource_record_name.setter
    def resource_record_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_record_name", value)

    @property
    @pulumi.getter(name="resourceRecordType")
    def resource_record_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of DNS record to create
        """
        return pulumi.get(self, "resource_record_type")

    @resource_record_type.setter
    def resource_record_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_record_type", value)

    @property
    @pulumi.getter(name="resourceRecordValue")
    def resource_record_value(self) -> Optional[pulumi.Input[str]]:
        """
        The value the DNS record needs to have
        """
        return pulumi.get(self, "resource_record_value")

    @resource_record_value.setter
    def resource_record_value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_record_value", value)


@pulumi.input_type
class CertificateOptionsArgs:
    def __init__(__self__, *,
                 certificate_transparency_logging_preference: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] certificate_transparency_logging_preference: Specifies whether certificate details should be added to a certificate transparency log. Valid values are `ENABLED` or `DISABLED`. See https://docs.aws.amazon.com/acm/latest/userguide/acm-concepts.html#concept-transparency for more details.
        """
        if certificate_transparency_logging_preference is not None:
            pulumi.set(__self__, "certificate_transparency_logging_preference", certificate_transparency_logging_preference)

    @property
    @pulumi.getter(name="certificateTransparencyLoggingPreference")
    def certificate_transparency_logging_preference(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies whether certificate details should be added to a certificate transparency log. Valid values are `ENABLED` or `DISABLED`. See https://docs.aws.amazon.com/acm/latest/userguide/acm-concepts.html#concept-transparency for more details.
        """
        return pulumi.get(self, "certificate_transparency_logging_preference")

    @certificate_transparency_logging_preference.setter
    def certificate_transparency_logging_preference(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "certificate_transparency_logging_preference", value)


