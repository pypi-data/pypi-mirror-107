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

__all__ = ['ConnectorArgs', 'Connector']

@pulumi.input_type
class ConnectorArgs:
    def __init__(__self__, *,
                 ip_cidr_range: Optional[pulumi.Input[str]] = None,
                 machine_type: Optional[pulumi.Input[str]] = None,
                 max_instances: Optional[pulumi.Input[int]] = None,
                 max_throughput: Optional[pulumi.Input[int]] = None,
                 min_instances: Optional[pulumi.Input[int]] = None,
                 min_throughput: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 subnet: Optional[pulumi.Input['ConnectorSubnetArgs']] = None):
        """
        The set of arguments for constructing a Connector resource.
        :param pulumi.Input[str] ip_cidr_range: The range of internal addresses that follows RFC 4632 notation. Example: `10.132.0.0/28`.
        :param pulumi.Input[str] machine_type: Machine type of VM Instance underlying connector. Default is e2-micro
        :param pulumi.Input[int] max_instances: Maximum value of instances in autoscaling group underlying the connector.
        :param pulumi.Input[int] max_throughput: Maximum throughput of the connector in Mbps, must be greater than `min_throughput`. Default is 1000.
        :param pulumi.Input[int] min_instances: Minimum value of instances in autoscaling group underlying the connector.
        :param pulumi.Input[int] min_throughput: Minimum throughput of the connector in Mbps. Default and min is 200.
        :param pulumi.Input[str] name: The name of the resource (Max 25 characters).
        :param pulumi.Input[str] network: Name of the VPC network. Required if `ip_cidr_range` is set.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: Region where the VPC Access connector resides. If it is not provided, the provider region is used.
        :param pulumi.Input['ConnectorSubnetArgs'] subnet: The subnet in which to house the connector
        """
        if ip_cidr_range is not None:
            pulumi.set(__self__, "ip_cidr_range", ip_cidr_range)
        if machine_type is not None:
            pulumi.set(__self__, "machine_type", machine_type)
        if max_instances is not None:
            pulumi.set(__self__, "max_instances", max_instances)
        if max_throughput is not None:
            pulumi.set(__self__, "max_throughput", max_throughput)
        if min_instances is not None:
            pulumi.set(__self__, "min_instances", min_instances)
        if min_throughput is not None:
            pulumi.set(__self__, "min_throughput", min_throughput)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if network is not None:
            pulumi.set(__self__, "network", network)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if region is not None:
            pulumi.set(__self__, "region", region)
        if subnet is not None:
            pulumi.set(__self__, "subnet", subnet)

    @property
    @pulumi.getter(name="ipCidrRange")
    def ip_cidr_range(self) -> Optional[pulumi.Input[str]]:
        """
        The range of internal addresses that follows RFC 4632 notation. Example: `10.132.0.0/28`.
        """
        return pulumi.get(self, "ip_cidr_range")

    @ip_cidr_range.setter
    def ip_cidr_range(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ip_cidr_range", value)

    @property
    @pulumi.getter(name="machineType")
    def machine_type(self) -> Optional[pulumi.Input[str]]:
        """
        Machine type of VM Instance underlying connector. Default is e2-micro
        """
        return pulumi.get(self, "machine_type")

    @machine_type.setter
    def machine_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "machine_type", value)

    @property
    @pulumi.getter(name="maxInstances")
    def max_instances(self) -> Optional[pulumi.Input[int]]:
        """
        Maximum value of instances in autoscaling group underlying the connector.
        """
        return pulumi.get(self, "max_instances")

    @max_instances.setter
    def max_instances(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_instances", value)

    @property
    @pulumi.getter(name="maxThroughput")
    def max_throughput(self) -> Optional[pulumi.Input[int]]:
        """
        Maximum throughput of the connector in Mbps, must be greater than `min_throughput`. Default is 1000.
        """
        return pulumi.get(self, "max_throughput")

    @max_throughput.setter
    def max_throughput(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_throughput", value)

    @property
    @pulumi.getter(name="minInstances")
    def min_instances(self) -> Optional[pulumi.Input[int]]:
        """
        Minimum value of instances in autoscaling group underlying the connector.
        """
        return pulumi.get(self, "min_instances")

    @min_instances.setter
    def min_instances(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "min_instances", value)

    @property
    @pulumi.getter(name="minThroughput")
    def min_throughput(self) -> Optional[pulumi.Input[int]]:
        """
        Minimum throughput of the connector in Mbps. Default and min is 200.
        """
        return pulumi.get(self, "min_throughput")

    @min_throughput.setter
    def min_throughput(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "min_throughput", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource (Max 25 characters).
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def network(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the VPC network. Required if `ip_cidr_range` is set.
        """
        return pulumi.get(self, "network")

    @network.setter
    def network(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "network", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter
    def region(self) -> Optional[pulumi.Input[str]]:
        """
        Region where the VPC Access connector resides. If it is not provided, the provider region is used.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)

    @property
    @pulumi.getter
    def subnet(self) -> Optional[pulumi.Input['ConnectorSubnetArgs']]:
        """
        The subnet in which to house the connector
        """
        return pulumi.get(self, "subnet")

    @subnet.setter
    def subnet(self, value: Optional[pulumi.Input['ConnectorSubnetArgs']]):
        pulumi.set(self, "subnet", value)


@pulumi.input_type
class _ConnectorState:
    def __init__(__self__, *,
                 ip_cidr_range: Optional[pulumi.Input[str]] = None,
                 machine_type: Optional[pulumi.Input[str]] = None,
                 max_instances: Optional[pulumi.Input[int]] = None,
                 max_throughput: Optional[pulumi.Input[int]] = None,
                 min_instances: Optional[pulumi.Input[int]] = None,
                 min_throughput: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 self_link: Optional[pulumi.Input[str]] = None,
                 state: Optional[pulumi.Input[str]] = None,
                 subnet: Optional[pulumi.Input['ConnectorSubnetArgs']] = None):
        """
        Input properties used for looking up and filtering Connector resources.
        :param pulumi.Input[str] ip_cidr_range: The range of internal addresses that follows RFC 4632 notation. Example: `10.132.0.0/28`.
        :param pulumi.Input[str] machine_type: Machine type of VM Instance underlying connector. Default is e2-micro
        :param pulumi.Input[int] max_instances: Maximum value of instances in autoscaling group underlying the connector.
        :param pulumi.Input[int] max_throughput: Maximum throughput of the connector in Mbps, must be greater than `min_throughput`. Default is 1000.
        :param pulumi.Input[int] min_instances: Minimum value of instances in autoscaling group underlying the connector.
        :param pulumi.Input[int] min_throughput: Minimum throughput of the connector in Mbps. Default and min is 200.
        :param pulumi.Input[str] name: The name of the resource (Max 25 characters).
        :param pulumi.Input[str] network: Name of the VPC network. Required if `ip_cidr_range` is set.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: Region where the VPC Access connector resides. If it is not provided, the provider region is used.
        :param pulumi.Input[str] self_link: The fully qualified name of this VPC connector
        :param pulumi.Input[str] state: State of the VPC access connector.
        :param pulumi.Input['ConnectorSubnetArgs'] subnet: The subnet in which to house the connector
        """
        if ip_cidr_range is not None:
            pulumi.set(__self__, "ip_cidr_range", ip_cidr_range)
        if machine_type is not None:
            pulumi.set(__self__, "machine_type", machine_type)
        if max_instances is not None:
            pulumi.set(__self__, "max_instances", max_instances)
        if max_throughput is not None:
            pulumi.set(__self__, "max_throughput", max_throughput)
        if min_instances is not None:
            pulumi.set(__self__, "min_instances", min_instances)
        if min_throughput is not None:
            pulumi.set(__self__, "min_throughput", min_throughput)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if network is not None:
            pulumi.set(__self__, "network", network)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if region is not None:
            pulumi.set(__self__, "region", region)
        if self_link is not None:
            pulumi.set(__self__, "self_link", self_link)
        if state is not None:
            pulumi.set(__self__, "state", state)
        if subnet is not None:
            pulumi.set(__self__, "subnet", subnet)

    @property
    @pulumi.getter(name="ipCidrRange")
    def ip_cidr_range(self) -> Optional[pulumi.Input[str]]:
        """
        The range of internal addresses that follows RFC 4632 notation. Example: `10.132.0.0/28`.
        """
        return pulumi.get(self, "ip_cidr_range")

    @ip_cidr_range.setter
    def ip_cidr_range(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ip_cidr_range", value)

    @property
    @pulumi.getter(name="machineType")
    def machine_type(self) -> Optional[pulumi.Input[str]]:
        """
        Machine type of VM Instance underlying connector. Default is e2-micro
        """
        return pulumi.get(self, "machine_type")

    @machine_type.setter
    def machine_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "machine_type", value)

    @property
    @pulumi.getter(name="maxInstances")
    def max_instances(self) -> Optional[pulumi.Input[int]]:
        """
        Maximum value of instances in autoscaling group underlying the connector.
        """
        return pulumi.get(self, "max_instances")

    @max_instances.setter
    def max_instances(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_instances", value)

    @property
    @pulumi.getter(name="maxThroughput")
    def max_throughput(self) -> Optional[pulumi.Input[int]]:
        """
        Maximum throughput of the connector in Mbps, must be greater than `min_throughput`. Default is 1000.
        """
        return pulumi.get(self, "max_throughput")

    @max_throughput.setter
    def max_throughput(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_throughput", value)

    @property
    @pulumi.getter(name="minInstances")
    def min_instances(self) -> Optional[pulumi.Input[int]]:
        """
        Minimum value of instances in autoscaling group underlying the connector.
        """
        return pulumi.get(self, "min_instances")

    @min_instances.setter
    def min_instances(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "min_instances", value)

    @property
    @pulumi.getter(name="minThroughput")
    def min_throughput(self) -> Optional[pulumi.Input[int]]:
        """
        Minimum throughput of the connector in Mbps. Default and min is 200.
        """
        return pulumi.get(self, "min_throughput")

    @min_throughput.setter
    def min_throughput(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "min_throughput", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource (Max 25 characters).
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def network(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the VPC network. Required if `ip_cidr_range` is set.
        """
        return pulumi.get(self, "network")

    @network.setter
    def network(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "network", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter
    def region(self) -> Optional[pulumi.Input[str]]:
        """
        Region where the VPC Access connector resides. If it is not provided, the provider region is used.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)

    @property
    @pulumi.getter(name="selfLink")
    def self_link(self) -> Optional[pulumi.Input[str]]:
        """
        The fully qualified name of this VPC connector
        """
        return pulumi.get(self, "self_link")

    @self_link.setter
    def self_link(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "self_link", value)

    @property
    @pulumi.getter
    def state(self) -> Optional[pulumi.Input[str]]:
        """
        State of the VPC access connector.
        """
        return pulumi.get(self, "state")

    @state.setter
    def state(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "state", value)

    @property
    @pulumi.getter
    def subnet(self) -> Optional[pulumi.Input['ConnectorSubnetArgs']]:
        """
        The subnet in which to house the connector
        """
        return pulumi.get(self, "subnet")

    @subnet.setter
    def subnet(self, value: Optional[pulumi.Input['ConnectorSubnetArgs']]):
        pulumi.set(self, "subnet", value)


class Connector(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 ip_cidr_range: Optional[pulumi.Input[str]] = None,
                 machine_type: Optional[pulumi.Input[str]] = None,
                 max_instances: Optional[pulumi.Input[int]] = None,
                 max_throughput: Optional[pulumi.Input[int]] = None,
                 min_instances: Optional[pulumi.Input[int]] = None,
                 min_throughput: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 subnet: Optional[pulumi.Input[pulumi.InputType['ConnectorSubnetArgs']]] = None,
                 __props__=None):
        """
        Serverless VPC Access connector resource.

        To get more information about Connector, see:

        * [API documentation](https://cloud.google.com/vpc/docs/reference/vpcaccess/rest/v1/projects.locations.connectors)
        * How-to Guides
            * [Configuring Serverless VPC Access](https://cloud.google.com/vpc/docs/configure-serverless-vpc-access)

        ## Example Usage
        ### VPC Access Connector

        ```python
        import pulumi
        import pulumi_gcp as gcp

        connector = gcp.vpcaccess.Connector("connector",
            ip_cidr_range="10.8.0.0/28",
            network="default")
        ```
        ### VPC Access Connector Shared VPC

        ```python
        import pulumi
        import pulumi_gcp as gcp

        custom_test_network = gcp.compute.Network("customTestNetwork", auto_create_subnetworks=False,
        opts=pulumi.ResourceOptions(provider=google_beta))
        custom_test_subnetwork = gcp.compute.Subnetwork("customTestSubnetwork",
            ip_cidr_range="10.2.0.0/28",
            region="us-central1",
            network=custom_test_network.id,
            opts=pulumi.ResourceOptions(provider=google_beta))
        connector = gcp.vpcaccess.Connector("connector",
            subnet=gcp.vpcaccess.ConnectorSubnetArgs(
                name=custom_test_subnetwork.name,
            ),
            machine_type="e2-standard-4",
            opts=pulumi.ResourceOptions(provider=google_beta))
        ```

        ## Import

        Connector can be imported using any of these accepted formats

        ```sh
         $ pulumi import gcp:vpcaccess/connector:Connector default projects/{{project}}/locations/{{region}}/connectors/{{name}}
        ```

        ```sh
         $ pulumi import gcp:vpcaccess/connector:Connector default {{project}}/{{region}}/{{name}}
        ```

        ```sh
         $ pulumi import gcp:vpcaccess/connector:Connector default {{region}}/{{name}}
        ```

        ```sh
         $ pulumi import gcp:vpcaccess/connector:Connector default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] ip_cidr_range: The range of internal addresses that follows RFC 4632 notation. Example: `10.132.0.0/28`.
        :param pulumi.Input[str] machine_type: Machine type of VM Instance underlying connector. Default is e2-micro
        :param pulumi.Input[int] max_instances: Maximum value of instances in autoscaling group underlying the connector.
        :param pulumi.Input[int] max_throughput: Maximum throughput of the connector in Mbps, must be greater than `min_throughput`. Default is 1000.
        :param pulumi.Input[int] min_instances: Minimum value of instances in autoscaling group underlying the connector.
        :param pulumi.Input[int] min_throughput: Minimum throughput of the connector in Mbps. Default and min is 200.
        :param pulumi.Input[str] name: The name of the resource (Max 25 characters).
        :param pulumi.Input[str] network: Name of the VPC network. Required if `ip_cidr_range` is set.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: Region where the VPC Access connector resides. If it is not provided, the provider region is used.
        :param pulumi.Input[pulumi.InputType['ConnectorSubnetArgs']] subnet: The subnet in which to house the connector
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[ConnectorArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Serverless VPC Access connector resource.

        To get more information about Connector, see:

        * [API documentation](https://cloud.google.com/vpc/docs/reference/vpcaccess/rest/v1/projects.locations.connectors)
        * How-to Guides
            * [Configuring Serverless VPC Access](https://cloud.google.com/vpc/docs/configure-serverless-vpc-access)

        ## Example Usage
        ### VPC Access Connector

        ```python
        import pulumi
        import pulumi_gcp as gcp

        connector = gcp.vpcaccess.Connector("connector",
            ip_cidr_range="10.8.0.0/28",
            network="default")
        ```
        ### VPC Access Connector Shared VPC

        ```python
        import pulumi
        import pulumi_gcp as gcp

        custom_test_network = gcp.compute.Network("customTestNetwork", auto_create_subnetworks=False,
        opts=pulumi.ResourceOptions(provider=google_beta))
        custom_test_subnetwork = gcp.compute.Subnetwork("customTestSubnetwork",
            ip_cidr_range="10.2.0.0/28",
            region="us-central1",
            network=custom_test_network.id,
            opts=pulumi.ResourceOptions(provider=google_beta))
        connector = gcp.vpcaccess.Connector("connector",
            subnet=gcp.vpcaccess.ConnectorSubnetArgs(
                name=custom_test_subnetwork.name,
            ),
            machine_type="e2-standard-4",
            opts=pulumi.ResourceOptions(provider=google_beta))
        ```

        ## Import

        Connector can be imported using any of these accepted formats

        ```sh
         $ pulumi import gcp:vpcaccess/connector:Connector default projects/{{project}}/locations/{{region}}/connectors/{{name}}
        ```

        ```sh
         $ pulumi import gcp:vpcaccess/connector:Connector default {{project}}/{{region}}/{{name}}
        ```

        ```sh
         $ pulumi import gcp:vpcaccess/connector:Connector default {{region}}/{{name}}
        ```

        ```sh
         $ pulumi import gcp:vpcaccess/connector:Connector default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param ConnectorArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ConnectorArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 ip_cidr_range: Optional[pulumi.Input[str]] = None,
                 machine_type: Optional[pulumi.Input[str]] = None,
                 max_instances: Optional[pulumi.Input[int]] = None,
                 max_throughput: Optional[pulumi.Input[int]] = None,
                 min_instances: Optional[pulumi.Input[int]] = None,
                 min_throughput: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 subnet: Optional[pulumi.Input[pulumi.InputType['ConnectorSubnetArgs']]] = None,
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
            __props__ = ConnectorArgs.__new__(ConnectorArgs)

            __props__.__dict__["ip_cidr_range"] = ip_cidr_range
            __props__.__dict__["machine_type"] = machine_type
            __props__.__dict__["max_instances"] = max_instances
            __props__.__dict__["max_throughput"] = max_throughput
            __props__.__dict__["min_instances"] = min_instances
            __props__.__dict__["min_throughput"] = min_throughput
            __props__.__dict__["name"] = name
            __props__.__dict__["network"] = network
            __props__.__dict__["project"] = project
            __props__.__dict__["region"] = region
            __props__.__dict__["subnet"] = subnet
            __props__.__dict__["self_link"] = None
            __props__.__dict__["state"] = None
        super(Connector, __self__).__init__(
            'gcp:vpcaccess/connector:Connector',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            ip_cidr_range: Optional[pulumi.Input[str]] = None,
            machine_type: Optional[pulumi.Input[str]] = None,
            max_instances: Optional[pulumi.Input[int]] = None,
            max_throughput: Optional[pulumi.Input[int]] = None,
            min_instances: Optional[pulumi.Input[int]] = None,
            min_throughput: Optional[pulumi.Input[int]] = None,
            name: Optional[pulumi.Input[str]] = None,
            network: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            region: Optional[pulumi.Input[str]] = None,
            self_link: Optional[pulumi.Input[str]] = None,
            state: Optional[pulumi.Input[str]] = None,
            subnet: Optional[pulumi.Input[pulumi.InputType['ConnectorSubnetArgs']]] = None) -> 'Connector':
        """
        Get an existing Connector resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] ip_cidr_range: The range of internal addresses that follows RFC 4632 notation. Example: `10.132.0.0/28`.
        :param pulumi.Input[str] machine_type: Machine type of VM Instance underlying connector. Default is e2-micro
        :param pulumi.Input[int] max_instances: Maximum value of instances in autoscaling group underlying the connector.
        :param pulumi.Input[int] max_throughput: Maximum throughput of the connector in Mbps, must be greater than `min_throughput`. Default is 1000.
        :param pulumi.Input[int] min_instances: Minimum value of instances in autoscaling group underlying the connector.
        :param pulumi.Input[int] min_throughput: Minimum throughput of the connector in Mbps. Default and min is 200.
        :param pulumi.Input[str] name: The name of the resource (Max 25 characters).
        :param pulumi.Input[str] network: Name of the VPC network. Required if `ip_cidr_range` is set.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: Region where the VPC Access connector resides. If it is not provided, the provider region is used.
        :param pulumi.Input[str] self_link: The fully qualified name of this VPC connector
        :param pulumi.Input[str] state: State of the VPC access connector.
        :param pulumi.Input[pulumi.InputType['ConnectorSubnetArgs']] subnet: The subnet in which to house the connector
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ConnectorState.__new__(_ConnectorState)

        __props__.__dict__["ip_cidr_range"] = ip_cidr_range
        __props__.__dict__["machine_type"] = machine_type
        __props__.__dict__["max_instances"] = max_instances
        __props__.__dict__["max_throughput"] = max_throughput
        __props__.__dict__["min_instances"] = min_instances
        __props__.__dict__["min_throughput"] = min_throughput
        __props__.__dict__["name"] = name
        __props__.__dict__["network"] = network
        __props__.__dict__["project"] = project
        __props__.__dict__["region"] = region
        __props__.__dict__["self_link"] = self_link
        __props__.__dict__["state"] = state
        __props__.__dict__["subnet"] = subnet
        return Connector(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="ipCidrRange")
    def ip_cidr_range(self) -> pulumi.Output[Optional[str]]:
        """
        The range of internal addresses that follows RFC 4632 notation. Example: `10.132.0.0/28`.
        """
        return pulumi.get(self, "ip_cidr_range")

    @property
    @pulumi.getter(name="machineType")
    def machine_type(self) -> pulumi.Output[Optional[str]]:
        """
        Machine type of VM Instance underlying connector. Default is e2-micro
        """
        return pulumi.get(self, "machine_type")

    @property
    @pulumi.getter(name="maxInstances")
    def max_instances(self) -> pulumi.Output[int]:
        """
        Maximum value of instances in autoscaling group underlying the connector.
        """
        return pulumi.get(self, "max_instances")

    @property
    @pulumi.getter(name="maxThroughput")
    def max_throughput(self) -> pulumi.Output[Optional[int]]:
        """
        Maximum throughput of the connector in Mbps, must be greater than `min_throughput`. Default is 1000.
        """
        return pulumi.get(self, "max_throughput")

    @property
    @pulumi.getter(name="minInstances")
    def min_instances(self) -> pulumi.Output[int]:
        """
        Minimum value of instances in autoscaling group underlying the connector.
        """
        return pulumi.get(self, "min_instances")

    @property
    @pulumi.getter(name="minThroughput")
    def min_throughput(self) -> pulumi.Output[Optional[int]]:
        """
        Minimum throughput of the connector in Mbps. Default and min is 200.
        """
        return pulumi.get(self, "min_throughput")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource (Max 25 characters).
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def network(self) -> pulumi.Output[Optional[str]]:
        """
        Name of the VPC network. Required if `ip_cidr_range` is set.
        """
        return pulumi.get(self, "network")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter
    def region(self) -> pulumi.Output[str]:
        """
        Region where the VPC Access connector resides. If it is not provided, the provider region is used.
        """
        return pulumi.get(self, "region")

    @property
    @pulumi.getter(name="selfLink")
    def self_link(self) -> pulumi.Output[str]:
        """
        The fully qualified name of this VPC connector
        """
        return pulumi.get(self, "self_link")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        State of the VPC access connector.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def subnet(self) -> pulumi.Output[Optional['outputs.ConnectorSubnet']]:
        """
        The subnet in which to house the connector
        """
        return pulumi.get(self, "subnet")

