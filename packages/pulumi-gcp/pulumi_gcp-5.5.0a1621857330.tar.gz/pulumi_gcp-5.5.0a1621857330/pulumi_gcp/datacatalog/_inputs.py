# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'EntryBigqueryDateShardedSpecArgs',
    'EntryBigqueryTableSpecArgs',
    'EntryBigqueryTableSpecTableSpecArgs',
    'EntryBigqueryTableSpecViewSpecArgs',
    'EntryGcsFilesetSpecArgs',
    'EntryGcsFilesetSpecSampleGcsFileSpecArgs',
    'EntryGroupIamBindingConditionArgs',
    'EntryGroupIamMemberConditionArgs',
    'PolicyTagIamBindingConditionArgs',
    'PolicyTagIamMemberConditionArgs',
    'TagFieldArgs',
    'TagTemplateFieldArgs',
    'TagTemplateFieldTypeArgs',
    'TagTemplateFieldTypeEnumTypeArgs',
    'TagTemplateFieldTypeEnumTypeAllowedValueArgs',
    'TagTemplateIamBindingConditionArgs',
    'TagTemplateIamMemberConditionArgs',
    'TaxonomyIamBindingConditionArgs',
    'TaxonomyIamMemberConditionArgs',
]

@pulumi.input_type
class EntryBigqueryDateShardedSpecArgs:
    def __init__(__self__, *,
                 dataset: Optional[pulumi.Input[str]] = None,
                 shard_count: Optional[pulumi.Input[int]] = None,
                 table_prefix: Optional[pulumi.Input[str]] = None):
        if dataset is not None:
            pulumi.set(__self__, "dataset", dataset)
        if shard_count is not None:
            pulumi.set(__self__, "shard_count", shard_count)
        if table_prefix is not None:
            pulumi.set(__self__, "table_prefix", table_prefix)

    @property
    @pulumi.getter
    def dataset(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "dataset")

    @dataset.setter
    def dataset(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "dataset", value)

    @property
    @pulumi.getter(name="shardCount")
    def shard_count(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "shard_count")

    @shard_count.setter
    def shard_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "shard_count", value)

    @property
    @pulumi.getter(name="tablePrefix")
    def table_prefix(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "table_prefix")

    @table_prefix.setter
    def table_prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "table_prefix", value)


@pulumi.input_type
class EntryBigqueryTableSpecArgs:
    def __init__(__self__, *,
                 table_source_type: Optional[pulumi.Input[str]] = None,
                 table_specs: Optional[pulumi.Input[Sequence[pulumi.Input['EntryBigqueryTableSpecTableSpecArgs']]]] = None,
                 view_specs: Optional[pulumi.Input[Sequence[pulumi.Input['EntryBigqueryTableSpecViewSpecArgs']]]] = None):
        if table_source_type is not None:
            pulumi.set(__self__, "table_source_type", table_source_type)
        if table_specs is not None:
            pulumi.set(__self__, "table_specs", table_specs)
        if view_specs is not None:
            pulumi.set(__self__, "view_specs", view_specs)

    @property
    @pulumi.getter(name="tableSourceType")
    def table_source_type(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "table_source_type")

    @table_source_type.setter
    def table_source_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "table_source_type", value)

    @property
    @pulumi.getter(name="tableSpecs")
    def table_specs(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['EntryBigqueryTableSpecTableSpecArgs']]]]:
        return pulumi.get(self, "table_specs")

    @table_specs.setter
    def table_specs(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['EntryBigqueryTableSpecTableSpecArgs']]]]):
        pulumi.set(self, "table_specs", value)

    @property
    @pulumi.getter(name="viewSpecs")
    def view_specs(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['EntryBigqueryTableSpecViewSpecArgs']]]]:
        return pulumi.get(self, "view_specs")

    @view_specs.setter
    def view_specs(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['EntryBigqueryTableSpecViewSpecArgs']]]]):
        pulumi.set(self, "view_specs", value)


@pulumi.input_type
class EntryBigqueryTableSpecTableSpecArgs:
    def __init__(__self__, *,
                 grouped_entry: Optional[pulumi.Input[str]] = None):
        if grouped_entry is not None:
            pulumi.set(__self__, "grouped_entry", grouped_entry)

    @property
    @pulumi.getter(name="groupedEntry")
    def grouped_entry(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "grouped_entry")

    @grouped_entry.setter
    def grouped_entry(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "grouped_entry", value)


@pulumi.input_type
class EntryBigqueryTableSpecViewSpecArgs:
    def __init__(__self__, *,
                 view_query: Optional[pulumi.Input[str]] = None):
        if view_query is not None:
            pulumi.set(__self__, "view_query", view_query)

    @property
    @pulumi.getter(name="viewQuery")
    def view_query(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "view_query")

    @view_query.setter
    def view_query(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "view_query", value)


@pulumi.input_type
class EntryGcsFilesetSpecArgs:
    def __init__(__self__, *,
                 file_patterns: pulumi.Input[Sequence[pulumi.Input[str]]],
                 sample_gcs_file_specs: Optional[pulumi.Input[Sequence[pulumi.Input['EntryGcsFilesetSpecSampleGcsFileSpecArgs']]]] = None):
        """
        :param pulumi.Input[Sequence[pulumi.Input[str]]] file_patterns: Patterns to identify a set of files in Google Cloud Storage.
               See [Cloud Storage documentation](https://cloud.google.com/storage/docs/gsutil/addlhelp/WildcardNames)
               for more information. Note that bucket wildcards are currently not supported. Examples of valid filePatterns:
               * gs://bucket_name/dir/*: matches all files within bucket_name/dir directory.
               * gs://bucket_name/dir/**: matches all files in bucket_name/dir spanning all subdirectories.
               * gs://bucket_name/file*: matches files prefixed by file in bucket_name
               * gs://bucket_name/??.txt: matches files with two characters followed by .txt in bucket_name
               * gs://bucket_name/[aeiou].txt: matches files that contain a single vowel character followed by .txt in bucket_name
               * gs://bucket_name/[a-m].txt: matches files that contain a, b, ... or m followed by .txt in bucket_name
               * gs://bucket_name/a/*/b: matches all files in bucket_name that match a/*/b pattern, such as a/c/b, a/d/b
               * gs://another_bucket/a.txt: matches gs://another_bucket/a.txt
        :param pulumi.Input[Sequence[pulumi.Input['EntryGcsFilesetSpecSampleGcsFileSpecArgs']]] sample_gcs_file_specs: -
               Sample files contained in this fileset, not all files contained in this fileset are represented here.
               Structure is documented below.
        """
        pulumi.set(__self__, "file_patterns", file_patterns)
        if sample_gcs_file_specs is not None:
            pulumi.set(__self__, "sample_gcs_file_specs", sample_gcs_file_specs)

    @property
    @pulumi.getter(name="filePatterns")
    def file_patterns(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        Patterns to identify a set of files in Google Cloud Storage.
        See [Cloud Storage documentation](https://cloud.google.com/storage/docs/gsutil/addlhelp/WildcardNames)
        for more information. Note that bucket wildcards are currently not supported. Examples of valid filePatterns:
        * gs://bucket_name/dir/*: matches all files within bucket_name/dir directory.
        * gs://bucket_name/dir/**: matches all files in bucket_name/dir spanning all subdirectories.
        * gs://bucket_name/file*: matches files prefixed by file in bucket_name
        * gs://bucket_name/??.txt: matches files with two characters followed by .txt in bucket_name
        * gs://bucket_name/[aeiou].txt: matches files that contain a single vowel character followed by .txt in bucket_name
        * gs://bucket_name/[a-m].txt: matches files that contain a, b, ... or m followed by .txt in bucket_name
        * gs://bucket_name/a/*/b: matches all files in bucket_name that match a/*/b pattern, such as a/c/b, a/d/b
        * gs://another_bucket/a.txt: matches gs://another_bucket/a.txt
        """
        return pulumi.get(self, "file_patterns")

    @file_patterns.setter
    def file_patterns(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "file_patterns", value)

    @property
    @pulumi.getter(name="sampleGcsFileSpecs")
    def sample_gcs_file_specs(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['EntryGcsFilesetSpecSampleGcsFileSpecArgs']]]]:
        """
        -
        Sample files contained in this fileset, not all files contained in this fileset are represented here.
        Structure is documented below.
        """
        return pulumi.get(self, "sample_gcs_file_specs")

    @sample_gcs_file_specs.setter
    def sample_gcs_file_specs(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['EntryGcsFilesetSpecSampleGcsFileSpecArgs']]]]):
        pulumi.set(self, "sample_gcs_file_specs", value)


@pulumi.input_type
class EntryGcsFilesetSpecSampleGcsFileSpecArgs:
    def __init__(__self__, *,
                 file_path: Optional[pulumi.Input[str]] = None,
                 size_bytes: Optional[pulumi.Input[int]] = None):
        """
        :param pulumi.Input[str] file_path: -
               The full file path
        :param pulumi.Input[int] size_bytes: -
               The size of the file, in bytes.
        """
        if file_path is not None:
            pulumi.set(__self__, "file_path", file_path)
        if size_bytes is not None:
            pulumi.set(__self__, "size_bytes", size_bytes)

    @property
    @pulumi.getter(name="filePath")
    def file_path(self) -> Optional[pulumi.Input[str]]:
        """
        -
        The full file path
        """
        return pulumi.get(self, "file_path")

    @file_path.setter
    def file_path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "file_path", value)

    @property
    @pulumi.getter(name="sizeBytes")
    def size_bytes(self) -> Optional[pulumi.Input[int]]:
        """
        -
        The size of the file, in bytes.
        """
        return pulumi.get(self, "size_bytes")

    @size_bytes.setter
    def size_bytes(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "size_bytes", value)


@pulumi.input_type
class EntryGroupIamBindingConditionArgs:
    def __init__(__self__, *,
                 expression: pulumi.Input[str],
                 title: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None):
        pulumi.set(__self__, "expression", expression)
        pulumi.set(__self__, "title", title)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def expression(self) -> pulumi.Input[str]:
        return pulumi.get(self, "expression")

    @expression.setter
    def expression(self, value: pulumi.Input[str]):
        pulumi.set(self, "expression", value)

    @property
    @pulumi.getter
    def title(self) -> pulumi.Input[str]:
        return pulumi.get(self, "title")

    @title.setter
    def title(self, value: pulumi.Input[str]):
        pulumi.set(self, "title", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)


@pulumi.input_type
class EntryGroupIamMemberConditionArgs:
    def __init__(__self__, *,
                 expression: pulumi.Input[str],
                 title: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None):
        pulumi.set(__self__, "expression", expression)
        pulumi.set(__self__, "title", title)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def expression(self) -> pulumi.Input[str]:
        return pulumi.get(self, "expression")

    @expression.setter
    def expression(self, value: pulumi.Input[str]):
        pulumi.set(self, "expression", value)

    @property
    @pulumi.getter
    def title(self) -> pulumi.Input[str]:
        return pulumi.get(self, "title")

    @title.setter
    def title(self, value: pulumi.Input[str]):
        pulumi.set(self, "title", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)


@pulumi.input_type
class PolicyTagIamBindingConditionArgs:
    def __init__(__self__, *,
                 expression: pulumi.Input[str],
                 title: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None):
        pulumi.set(__self__, "expression", expression)
        pulumi.set(__self__, "title", title)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def expression(self) -> pulumi.Input[str]:
        return pulumi.get(self, "expression")

    @expression.setter
    def expression(self, value: pulumi.Input[str]):
        pulumi.set(self, "expression", value)

    @property
    @pulumi.getter
    def title(self) -> pulumi.Input[str]:
        return pulumi.get(self, "title")

    @title.setter
    def title(self, value: pulumi.Input[str]):
        pulumi.set(self, "title", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)


@pulumi.input_type
class PolicyTagIamMemberConditionArgs:
    def __init__(__self__, *,
                 expression: pulumi.Input[str],
                 title: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None):
        pulumi.set(__self__, "expression", expression)
        pulumi.set(__self__, "title", title)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def expression(self) -> pulumi.Input[str]:
        return pulumi.get(self, "expression")

    @expression.setter
    def expression(self, value: pulumi.Input[str]):
        pulumi.set(self, "expression", value)

    @property
    @pulumi.getter
    def title(self) -> pulumi.Input[str]:
        return pulumi.get(self, "title")

    @title.setter
    def title(self, value: pulumi.Input[str]):
        pulumi.set(self, "title", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)


@pulumi.input_type
class TagFieldArgs:
    def __init__(__self__, *,
                 field_name: pulumi.Input[str],
                 bool_value: Optional[pulumi.Input[bool]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 double_value: Optional[pulumi.Input[float]] = None,
                 enum_value: Optional[pulumi.Input[str]] = None,
                 order: Optional[pulumi.Input[int]] = None,
                 string_value: Optional[pulumi.Input[str]] = None,
                 timestamp_value: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] field_name: The identifier for this object. Format specified above.
        :param pulumi.Input[bool] bool_value: Holds the value for a tag field with boolean type.
        :param pulumi.Input[str] display_name: -
               The display name of this field
        :param pulumi.Input[float] double_value: Holds the value for a tag field with double type.
        :param pulumi.Input[str] enum_value: Holds the value for a tag field with enum type. This value must be one of the allowed values in the definition of this enum.
               Structure is documented below.
        :param pulumi.Input[int] order: -
               The order of this field with respect to other fields in this tag. For example, a higher value can indicate
               a more important field. The value can be negative. Multiple fields can have the same order, and field orders
               within a tag do not have to be sequential.
        :param pulumi.Input[str] string_value: Holds the value for a tag field with string type.
        :param pulumi.Input[str] timestamp_value: Holds the value for a tag field with timestamp type.
        """
        pulumi.set(__self__, "field_name", field_name)
        if bool_value is not None:
            pulumi.set(__self__, "bool_value", bool_value)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if double_value is not None:
            pulumi.set(__self__, "double_value", double_value)
        if enum_value is not None:
            pulumi.set(__self__, "enum_value", enum_value)
        if order is not None:
            pulumi.set(__self__, "order", order)
        if string_value is not None:
            pulumi.set(__self__, "string_value", string_value)
        if timestamp_value is not None:
            pulumi.set(__self__, "timestamp_value", timestamp_value)

    @property
    @pulumi.getter(name="fieldName")
    def field_name(self) -> pulumi.Input[str]:
        """
        The identifier for this object. Format specified above.
        """
        return pulumi.get(self, "field_name")

    @field_name.setter
    def field_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "field_name", value)

    @property
    @pulumi.getter(name="boolValue")
    def bool_value(self) -> Optional[pulumi.Input[bool]]:
        """
        Holds the value for a tag field with boolean type.
        """
        return pulumi.get(self, "bool_value")

    @bool_value.setter
    def bool_value(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "bool_value", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        -
        The display name of this field
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter(name="doubleValue")
    def double_value(self) -> Optional[pulumi.Input[float]]:
        """
        Holds the value for a tag field with double type.
        """
        return pulumi.get(self, "double_value")

    @double_value.setter
    def double_value(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "double_value", value)

    @property
    @pulumi.getter(name="enumValue")
    def enum_value(self) -> Optional[pulumi.Input[str]]:
        """
        Holds the value for a tag field with enum type. This value must be one of the allowed values in the definition of this enum.
        Structure is documented below.
        """
        return pulumi.get(self, "enum_value")

    @enum_value.setter
    def enum_value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "enum_value", value)

    @property
    @pulumi.getter
    def order(self) -> Optional[pulumi.Input[int]]:
        """
        -
        The order of this field with respect to other fields in this tag. For example, a higher value can indicate
        a more important field. The value can be negative. Multiple fields can have the same order, and field orders
        within a tag do not have to be sequential.
        """
        return pulumi.get(self, "order")

    @order.setter
    def order(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "order", value)

    @property
    @pulumi.getter(name="stringValue")
    def string_value(self) -> Optional[pulumi.Input[str]]:
        """
        Holds the value for a tag field with string type.
        """
        return pulumi.get(self, "string_value")

    @string_value.setter
    def string_value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "string_value", value)

    @property
    @pulumi.getter(name="timestampValue")
    def timestamp_value(self) -> Optional[pulumi.Input[str]]:
        """
        Holds the value for a tag field with timestamp type.
        """
        return pulumi.get(self, "timestamp_value")

    @timestamp_value.setter
    def timestamp_value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "timestamp_value", value)


@pulumi.input_type
class TagTemplateFieldArgs:
    def __init__(__self__, *,
                 field_id: pulumi.Input[str],
                 type: pulumi.Input['TagTemplateFieldTypeArgs'],
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 is_required: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 order: Optional[pulumi.Input[int]] = None):
        """
        :param pulumi.Input[str] field_id: The identifier for this object. Format specified above.
        :param pulumi.Input['TagTemplateFieldTypeArgs'] type: The type of value this tag field can contain.
               Structure is documented below.
        :param pulumi.Input[str] description: A description for this field.
        :param pulumi.Input[str] display_name: The display name for this template.
        :param pulumi.Input[bool] is_required: Whether this is a required field. Defaults to false.
        :param pulumi.Input[str] name: -
               The resource name of the tag template field in URL format. Example: projects/{project_id}/locations/{location}/tagTemplates/{tagTemplateId}/fields/{field}
        :param pulumi.Input[int] order: The order of this field with respect to other fields in this tag template.
               A higher value indicates a more important field. The value can be negative.
               Multiple fields can have the same order, and field orders within a tag do not have to be sequential.
        """
        pulumi.set(__self__, "field_id", field_id)
        pulumi.set(__self__, "type", type)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if is_required is not None:
            pulumi.set(__self__, "is_required", is_required)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if order is not None:
            pulumi.set(__self__, "order", order)

    @property
    @pulumi.getter(name="fieldId")
    def field_id(self) -> pulumi.Input[str]:
        """
        The identifier for this object. Format specified above.
        """
        return pulumi.get(self, "field_id")

    @field_id.setter
    def field_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "field_id", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input['TagTemplateFieldTypeArgs']:
        """
        The type of value this tag field can contain.
        Structure is documented below.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input['TagTemplateFieldTypeArgs']):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description for this field.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        The display name for this template.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter(name="isRequired")
    def is_required(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether this is a required field. Defaults to false.
        """
        return pulumi.get(self, "is_required")

    @is_required.setter
    def is_required(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_required", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        -
        The resource name of the tag template field in URL format. Example: projects/{project_id}/locations/{location}/tagTemplates/{tagTemplateId}/fields/{field}
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def order(self) -> Optional[pulumi.Input[int]]:
        """
        The order of this field with respect to other fields in this tag template.
        A higher value indicates a more important field. The value can be negative.
        Multiple fields can have the same order, and field orders within a tag do not have to be sequential.
        """
        return pulumi.get(self, "order")

    @order.setter
    def order(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "order", value)


@pulumi.input_type
class TagTemplateFieldTypeArgs:
    def __init__(__self__, *,
                 enum_type: Optional[pulumi.Input['TagTemplateFieldTypeEnumTypeArgs']] = None,
                 primitive_type: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input['TagTemplateFieldTypeEnumTypeArgs'] enum_type: Represents an enum type.
               Exactly one of `primitive_type` or `enum_type` must be set
               Structure is documented below.
        :param pulumi.Input[str] primitive_type: Represents primitive types - string, bool etc.
               Exactly one of `primitive_type` or `enum_type` must be set
               Possible values are `DOUBLE`, `STRING`, `BOOL`, and `TIMESTAMP`.
        """
        if enum_type is not None:
            pulumi.set(__self__, "enum_type", enum_type)
        if primitive_type is not None:
            pulumi.set(__self__, "primitive_type", primitive_type)

    @property
    @pulumi.getter(name="enumType")
    def enum_type(self) -> Optional[pulumi.Input['TagTemplateFieldTypeEnumTypeArgs']]:
        """
        Represents an enum type.
        Exactly one of `primitive_type` or `enum_type` must be set
        Structure is documented below.
        """
        return pulumi.get(self, "enum_type")

    @enum_type.setter
    def enum_type(self, value: Optional[pulumi.Input['TagTemplateFieldTypeEnumTypeArgs']]):
        pulumi.set(self, "enum_type", value)

    @property
    @pulumi.getter(name="primitiveType")
    def primitive_type(self) -> Optional[pulumi.Input[str]]:
        """
        Represents primitive types - string, bool etc.
        Exactly one of `primitive_type` or `enum_type` must be set
        Possible values are `DOUBLE`, `STRING`, `BOOL`, and `TIMESTAMP`.
        """
        return pulumi.get(self, "primitive_type")

    @primitive_type.setter
    def primitive_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "primitive_type", value)


@pulumi.input_type
class TagTemplateFieldTypeEnumTypeArgs:
    def __init__(__self__, *,
                 allowed_values: pulumi.Input[Sequence[pulumi.Input['TagTemplateFieldTypeEnumTypeAllowedValueArgs']]]):
        """
        :param pulumi.Input[Sequence[pulumi.Input['TagTemplateFieldTypeEnumTypeAllowedValueArgs']]] allowed_values: The set of allowed values for this enum. The display names of the
               values must be case-insensitively unique within this set. Currently,
               enum values can only be added to the list of allowed values. Deletion
               and renaming of enum values are not supported.
               Can have up to 500 allowed values.
               Structure is documented below.
        """
        pulumi.set(__self__, "allowed_values", allowed_values)

    @property
    @pulumi.getter(name="allowedValues")
    def allowed_values(self) -> pulumi.Input[Sequence[pulumi.Input['TagTemplateFieldTypeEnumTypeAllowedValueArgs']]]:
        """
        The set of allowed values for this enum. The display names of the
        values must be case-insensitively unique within this set. Currently,
        enum values can only be added to the list of allowed values. Deletion
        and renaming of enum values are not supported.
        Can have up to 500 allowed values.
        Structure is documented below.
        """
        return pulumi.get(self, "allowed_values")

    @allowed_values.setter
    def allowed_values(self, value: pulumi.Input[Sequence[pulumi.Input['TagTemplateFieldTypeEnumTypeAllowedValueArgs']]]):
        pulumi.set(self, "allowed_values", value)


@pulumi.input_type
class TagTemplateFieldTypeEnumTypeAllowedValueArgs:
    def __init__(__self__, *,
                 display_name: pulumi.Input[str]):
        """
        :param pulumi.Input[str] display_name: The display name for this template.
        """
        pulumi.set(__self__, "display_name", display_name)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Input[str]:
        """
        The display name for this template.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "display_name", value)


@pulumi.input_type
class TagTemplateIamBindingConditionArgs:
    def __init__(__self__, *,
                 expression: pulumi.Input[str],
                 title: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None):
        pulumi.set(__self__, "expression", expression)
        pulumi.set(__self__, "title", title)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def expression(self) -> pulumi.Input[str]:
        return pulumi.get(self, "expression")

    @expression.setter
    def expression(self, value: pulumi.Input[str]):
        pulumi.set(self, "expression", value)

    @property
    @pulumi.getter
    def title(self) -> pulumi.Input[str]:
        return pulumi.get(self, "title")

    @title.setter
    def title(self, value: pulumi.Input[str]):
        pulumi.set(self, "title", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)


@pulumi.input_type
class TagTemplateIamMemberConditionArgs:
    def __init__(__self__, *,
                 expression: pulumi.Input[str],
                 title: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None):
        pulumi.set(__self__, "expression", expression)
        pulumi.set(__self__, "title", title)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def expression(self) -> pulumi.Input[str]:
        return pulumi.get(self, "expression")

    @expression.setter
    def expression(self, value: pulumi.Input[str]):
        pulumi.set(self, "expression", value)

    @property
    @pulumi.getter
    def title(self) -> pulumi.Input[str]:
        return pulumi.get(self, "title")

    @title.setter
    def title(self, value: pulumi.Input[str]):
        pulumi.set(self, "title", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)


@pulumi.input_type
class TaxonomyIamBindingConditionArgs:
    def __init__(__self__, *,
                 expression: pulumi.Input[str],
                 title: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None):
        pulumi.set(__self__, "expression", expression)
        pulumi.set(__self__, "title", title)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def expression(self) -> pulumi.Input[str]:
        return pulumi.get(self, "expression")

    @expression.setter
    def expression(self, value: pulumi.Input[str]):
        pulumi.set(self, "expression", value)

    @property
    @pulumi.getter
    def title(self) -> pulumi.Input[str]:
        return pulumi.get(self, "title")

    @title.setter
    def title(self, value: pulumi.Input[str]):
        pulumi.set(self, "title", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)


@pulumi.input_type
class TaxonomyIamMemberConditionArgs:
    def __init__(__self__, *,
                 expression: pulumi.Input[str],
                 title: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None):
        pulumi.set(__self__, "expression", expression)
        pulumi.set(__self__, "title", title)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def expression(self) -> pulumi.Input[str]:
        return pulumi.get(self, "expression")

    @expression.setter
    def expression(self, value: pulumi.Input[str]):
        pulumi.set(self, "expression", value)

    @property
    @pulumi.getter
    def title(self) -> pulumi.Input[str]:
        return pulumi.get(self, "title")

    @title.setter
    def title(self, value: pulumi.Input[str]):
        pulumi.set(self, "title", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)


