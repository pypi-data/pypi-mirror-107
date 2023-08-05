# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'CryptoKeyIAMBindingConditionArgs',
    'CryptoKeyIAMMemberConditionArgs',
    'CryptoKeyVersionTemplateArgs',
    'KeyRingIAMBindingConditionArgs',
    'KeyRingIAMMemberConditionArgs',
    'KeyRingImportJobAttestationArgs',
    'KeyRingImportJobPublicKeyArgs',
    'RegistryCredentialArgs',
    'RegistryEventNotificationConfigItemArgs',
]

@pulumi.input_type
class CryptoKeyIAMBindingConditionArgs:
    def __init__(__self__, *,
                 expression: pulumi.Input[str],
                 title: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] expression: Textual representation of an expression in Common Expression Language syntax.
        :param pulumi.Input[str] title: A title for the expression, i.e. a short string describing its purpose.
        :param pulumi.Input[str] description: An optional description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI.
        """
        pulumi.set(__self__, "expression", expression)
        pulumi.set(__self__, "title", title)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def expression(self) -> pulumi.Input[str]:
        """
        Textual representation of an expression in Common Expression Language syntax.
        """
        return pulumi.get(self, "expression")

    @expression.setter
    def expression(self, value: pulumi.Input[str]):
        pulumi.set(self, "expression", value)

    @property
    @pulumi.getter
    def title(self) -> pulumi.Input[str]:
        """
        A title for the expression, i.e. a short string describing its purpose.
        """
        return pulumi.get(self, "title")

    @title.setter
    def title(self, value: pulumi.Input[str]):
        pulumi.set(self, "title", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        An optional description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)


@pulumi.input_type
class CryptoKeyIAMMemberConditionArgs:
    def __init__(__self__, *,
                 expression: pulumi.Input[str],
                 title: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] expression: Textual representation of an expression in Common Expression Language syntax.
        :param pulumi.Input[str] title: A title for the expression, i.e. a short string describing its purpose.
        :param pulumi.Input[str] description: An optional description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI.
        """
        pulumi.set(__self__, "expression", expression)
        pulumi.set(__self__, "title", title)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def expression(self) -> pulumi.Input[str]:
        """
        Textual representation of an expression in Common Expression Language syntax.
        """
        return pulumi.get(self, "expression")

    @expression.setter
    def expression(self, value: pulumi.Input[str]):
        pulumi.set(self, "expression", value)

    @property
    @pulumi.getter
    def title(self) -> pulumi.Input[str]:
        """
        A title for the expression, i.e. a short string describing its purpose.
        """
        return pulumi.get(self, "title")

    @title.setter
    def title(self, value: pulumi.Input[str]):
        pulumi.set(self, "title", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        An optional description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)


@pulumi.input_type
class CryptoKeyVersionTemplateArgs:
    def __init__(__self__, *,
                 algorithm: pulumi.Input[str],
                 protection_level: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] algorithm: The algorithm to use when creating a version based on this template.
               See the [algorithm reference](https://cloud.google.com/kms/docs/reference/rest/v1/CryptoKeyVersionAlgorithm) for possible inputs.
        :param pulumi.Input[str] protection_level: The protection level to use when creating a version based on this template.
               Default value is `SOFTWARE`.
               Possible values are `SOFTWARE` and `HSM`.
        """
        pulumi.set(__self__, "algorithm", algorithm)
        if protection_level is not None:
            pulumi.set(__self__, "protection_level", protection_level)

    @property
    @pulumi.getter
    def algorithm(self) -> pulumi.Input[str]:
        """
        The algorithm to use when creating a version based on this template.
        See the [algorithm reference](https://cloud.google.com/kms/docs/reference/rest/v1/CryptoKeyVersionAlgorithm) for possible inputs.
        """
        return pulumi.get(self, "algorithm")

    @algorithm.setter
    def algorithm(self, value: pulumi.Input[str]):
        pulumi.set(self, "algorithm", value)

    @property
    @pulumi.getter(name="protectionLevel")
    def protection_level(self) -> Optional[pulumi.Input[str]]:
        """
        The protection level to use when creating a version based on this template.
        Default value is `SOFTWARE`.
        Possible values are `SOFTWARE` and `HSM`.
        """
        return pulumi.get(self, "protection_level")

    @protection_level.setter
    def protection_level(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "protection_level", value)


@pulumi.input_type
class KeyRingIAMBindingConditionArgs:
    def __init__(__self__, *,
                 expression: pulumi.Input[str],
                 title: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] expression: Textual representation of an expression in Common Expression Language syntax.
        :param pulumi.Input[str] title: A title for the expression, i.e. a short string describing its purpose.
        :param pulumi.Input[str] description: An optional description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI.
        """
        pulumi.set(__self__, "expression", expression)
        pulumi.set(__self__, "title", title)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def expression(self) -> pulumi.Input[str]:
        """
        Textual representation of an expression in Common Expression Language syntax.
        """
        return pulumi.get(self, "expression")

    @expression.setter
    def expression(self, value: pulumi.Input[str]):
        pulumi.set(self, "expression", value)

    @property
    @pulumi.getter
    def title(self) -> pulumi.Input[str]:
        """
        A title for the expression, i.e. a short string describing its purpose.
        """
        return pulumi.get(self, "title")

    @title.setter
    def title(self, value: pulumi.Input[str]):
        pulumi.set(self, "title", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        An optional description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)


@pulumi.input_type
class KeyRingIAMMemberConditionArgs:
    def __init__(__self__, *,
                 expression: pulumi.Input[str],
                 title: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] expression: Textual representation of an expression in Common Expression Language syntax.
        :param pulumi.Input[str] title: A title for the expression, i.e. a short string describing its purpose.
        :param pulumi.Input[str] description: An optional description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI.
        """
        pulumi.set(__self__, "expression", expression)
        pulumi.set(__self__, "title", title)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def expression(self) -> pulumi.Input[str]:
        """
        Textual representation of an expression in Common Expression Language syntax.
        """
        return pulumi.get(self, "expression")

    @expression.setter
    def expression(self, value: pulumi.Input[str]):
        pulumi.set(self, "expression", value)

    @property
    @pulumi.getter
    def title(self) -> pulumi.Input[str]:
        """
        A title for the expression, i.e. a short string describing its purpose.
        """
        return pulumi.get(self, "title")

    @title.setter
    def title(self, value: pulumi.Input[str]):
        pulumi.set(self, "title", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        An optional description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)


@pulumi.input_type
class KeyRingImportJobAttestationArgs:
    def __init__(__self__, *,
                 content: Optional[pulumi.Input[str]] = None,
                 format: Optional[pulumi.Input[str]] = None):
        if content is not None:
            pulumi.set(__self__, "content", content)
        if format is not None:
            pulumi.set(__self__, "format", format)

    @property
    @pulumi.getter
    def content(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "content")

    @content.setter
    def content(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "content", value)

    @property
    @pulumi.getter
    def format(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "format")

    @format.setter
    def format(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "format", value)


@pulumi.input_type
class KeyRingImportJobPublicKeyArgs:
    def __init__(__self__, *,
                 pem: Optional[pulumi.Input[str]] = None):
        if pem is not None:
            pulumi.set(__self__, "pem", pem)

    @property
    @pulumi.getter
    def pem(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "pem")

    @pem.setter
    def pem(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "pem", value)


@pulumi.input_type
class RegistryCredentialArgs:
    def __init__(__self__, *,
                 public_key_certificate: pulumi.Input[Mapping[str, Any]]):
        """
        :param pulumi.Input[Mapping[str, Any]] public_key_certificate: A public key certificate format and data.
        """
        pulumi.set(__self__, "public_key_certificate", public_key_certificate)

    @property
    @pulumi.getter(name="publicKeyCertificate")
    def public_key_certificate(self) -> pulumi.Input[Mapping[str, Any]]:
        """
        A public key certificate format and data.
        """
        return pulumi.get(self, "public_key_certificate")

    @public_key_certificate.setter
    def public_key_certificate(self, value: pulumi.Input[Mapping[str, Any]]):
        pulumi.set(self, "public_key_certificate", value)


@pulumi.input_type
class RegistryEventNotificationConfigItemArgs:
    def __init__(__self__, *,
                 pubsub_topic_name: pulumi.Input[str],
                 subfolder_matches: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] pubsub_topic_name: PubSub topic name to publish device events.
        :param pulumi.Input[str] subfolder_matches: If the subfolder name matches this string exactly, this
               configuration will be used. The string must not include the
               leading '/' character. If empty, all strings are matched. Empty
               value can only be used for the last `event_notification_configs`
               item.
        """
        pulumi.set(__self__, "pubsub_topic_name", pubsub_topic_name)
        if subfolder_matches is not None:
            pulumi.set(__self__, "subfolder_matches", subfolder_matches)

    @property
    @pulumi.getter(name="pubsubTopicName")
    def pubsub_topic_name(self) -> pulumi.Input[str]:
        """
        PubSub topic name to publish device events.
        """
        return pulumi.get(self, "pubsub_topic_name")

    @pubsub_topic_name.setter
    def pubsub_topic_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "pubsub_topic_name", value)

    @property
    @pulumi.getter(name="subfolderMatches")
    def subfolder_matches(self) -> Optional[pulumi.Input[str]]:
        """
        If the subfolder name matches this string exactly, this
        configuration will be used. The string must not include the
        leading '/' character. If empty, all strings are matched. Empty
        value can only be used for the last `event_notification_configs`
        item.
        """
        return pulumi.get(self, "subfolder_matches")

    @subfolder_matches.setter
    def subfolder_matches(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "subfolder_matches", value)


