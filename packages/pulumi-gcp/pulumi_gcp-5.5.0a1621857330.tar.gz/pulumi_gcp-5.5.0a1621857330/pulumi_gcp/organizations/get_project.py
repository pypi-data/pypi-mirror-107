# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetProjectResult',
    'AwaitableGetProjectResult',
    'get_project',
]

@pulumi.output_type
class GetProjectResult:
    """
    A collection of values returned by getProject.
    """
    def __init__(__self__, auto_create_network=None, billing_account=None, folder_id=None, id=None, labels=None, name=None, number=None, org_id=None, project_id=None, skip_delete=None):
        if auto_create_network and not isinstance(auto_create_network, bool):
            raise TypeError("Expected argument 'auto_create_network' to be a bool")
        pulumi.set(__self__, "auto_create_network", auto_create_network)
        if billing_account and not isinstance(billing_account, str):
            raise TypeError("Expected argument 'billing_account' to be a str")
        pulumi.set(__self__, "billing_account", billing_account)
        if folder_id and not isinstance(folder_id, str):
            raise TypeError("Expected argument 'folder_id' to be a str")
        pulumi.set(__self__, "folder_id", folder_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if labels and not isinstance(labels, dict):
            raise TypeError("Expected argument 'labels' to be a dict")
        pulumi.set(__self__, "labels", labels)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if number and not isinstance(number, str):
            raise TypeError("Expected argument 'number' to be a str")
        pulumi.set(__self__, "number", number)
        if org_id and not isinstance(org_id, str):
            raise TypeError("Expected argument 'org_id' to be a str")
        pulumi.set(__self__, "org_id", org_id)
        if project_id and not isinstance(project_id, str):
            raise TypeError("Expected argument 'project_id' to be a str")
        pulumi.set(__self__, "project_id", project_id)
        if skip_delete and not isinstance(skip_delete, bool):
            raise TypeError("Expected argument 'skip_delete' to be a bool")
        pulumi.set(__self__, "skip_delete", skip_delete)

    @property
    @pulumi.getter(name="autoCreateNetwork")
    def auto_create_network(self) -> bool:
        return pulumi.get(self, "auto_create_network")

    @property
    @pulumi.getter(name="billingAccount")
    def billing_account(self) -> str:
        return pulumi.get(self, "billing_account")

    @property
    @pulumi.getter(name="folderId")
    def folder_id(self) -> str:
        return pulumi.get(self, "folder_id")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def labels(self) -> Mapping[str, str]:
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def number(self) -> str:
        return pulumi.get(self, "number")

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> str:
        return pulumi.get(self, "org_id")

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> Optional[str]:
        return pulumi.get(self, "project_id")

    @property
    @pulumi.getter(name="skipDelete")
    def skip_delete(self) -> bool:
        return pulumi.get(self, "skip_delete")


class AwaitableGetProjectResult(GetProjectResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetProjectResult(
            auto_create_network=self.auto_create_network,
            billing_account=self.billing_account,
            folder_id=self.folder_id,
            id=self.id,
            labels=self.labels,
            name=self.name,
            number=self.number,
            org_id=self.org_id,
            project_id=self.project_id,
            skip_delete=self.skip_delete)


def get_project(project_id: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetProjectResult:
    """
    Use this data source to get project details.
    For more information see
    [API](https://cloud.google.com/resource-manager/reference/rest/v1/projects#Project)

    ## Example Usage

    ```python
    import pulumi
    import pulumi_gcp as gcp

    project = gcp.organizations.get_project()
    pulumi.export("projectNumber", project.number)
    ```


    :param str project_id: The project ID. If it is not provided, the provider project is used.
    """
    __args__ = dict()
    __args__['projectId'] = project_id
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('gcp:organizations/getProject:getProject', __args__, opts=opts, typ=GetProjectResult).value

    return AwaitableGetProjectResult(
        auto_create_network=__ret__.auto_create_network,
        billing_account=__ret__.billing_account,
        folder_id=__ret__.folder_id,
        id=__ret__.id,
        labels=__ret__.labels,
        name=__ret__.name,
        number=__ret__.number,
        org_id=__ret__.org_id,
        project_id=__ret__.project_id,
        skip_delete=__ret__.skip_delete)
