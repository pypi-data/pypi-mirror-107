# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetSolutionStackResult',
    'AwaitableGetSolutionStackResult',
    'get_solution_stack',
]

@pulumi.output_type
class GetSolutionStackResult:
    """
    A collection of values returned by getSolutionStack.
    """
    def __init__(__self__, id=None, most_recent=None, name=None, name_regex=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if most_recent and not isinstance(most_recent, bool):
            raise TypeError("Expected argument 'most_recent' to be a bool")
        pulumi.set(__self__, "most_recent", most_recent)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if name_regex and not isinstance(name_regex, str):
            raise TypeError("Expected argument 'name_regex' to be a str")
        pulumi.set(__self__, "name_regex", name_regex)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="mostRecent")
    def most_recent(self) -> Optional[bool]:
        return pulumi.get(self, "most_recent")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the solution stack.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="nameRegex")
    def name_regex(self) -> str:
        return pulumi.get(self, "name_regex")


class AwaitableGetSolutionStackResult(GetSolutionStackResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSolutionStackResult(
            id=self.id,
            most_recent=self.most_recent,
            name=self.name,
            name_regex=self.name_regex)


def get_solution_stack(most_recent: Optional[bool] = None,
                       name_regex: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSolutionStackResult:
    """
    Use this data source to get the name of a elastic beanstalk solution stack.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    multi_docker = aws.elasticbeanstalk.get_solution_stack(most_recent=True,
        name_regex="^64bit Amazon Linux (.*) Multi-container Docker (.*)$")
    ```


    :param bool most_recent: If more than one result is returned, use the most
           recent solution stack.
    :param str name_regex: A regex string to apply to the solution stack list returned
           by AWS. See [Elastic Beanstalk Supported Platforms][beanstalk-platforms] from
           AWS documentation for reference solution stack names.
    """
    __args__ = dict()
    __args__['mostRecent'] = most_recent
    __args__['nameRegex'] = name_regex
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws:elasticbeanstalk/getSolutionStack:getSolutionStack', __args__, opts=opts, typ=GetSolutionStackResult).value

    return AwaitableGetSolutionStackResult(
        id=__ret__.id,
        most_recent=__ret__.most_recent,
        name=__ret__.name,
        name_regex=__ret__.name_regex)
