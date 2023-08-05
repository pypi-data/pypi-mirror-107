# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from .agent import *
from .entity_type import *
from .intent import *
from ._inputs import *
from . import outputs

def _register_module():
    import pulumi
    from .. import _utilities


    class Module(pulumi.runtime.ResourceModule):
        _version = _utilities.get_semver_version()

        def version(self):
            return Module._version

        def construct(self, name: str, typ: str, urn: str) -> pulumi.Resource:
            if typ == "gcp:diagflow/agent:Agent":
                return Agent(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "gcp:diagflow/entityType:EntityType":
                return EntityType(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "gcp:diagflow/intent:Intent":
                return Intent(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("gcp", "diagflow/agent", _module_instance)
    pulumi.runtime.register_resource_module("gcp", "diagflow/entityType", _module_instance)
    pulumi.runtime.register_resource_module("gcp", "diagflow/intent", _module_instance)

_register_module()
