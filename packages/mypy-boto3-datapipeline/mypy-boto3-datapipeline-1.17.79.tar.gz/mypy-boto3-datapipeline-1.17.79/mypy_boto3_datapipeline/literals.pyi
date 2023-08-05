"""
Type annotations for datapipeline service literal definitions.

[Open documentation](./literals.md)

Usage::

    ```python
    from mypy_boto3_datapipeline.literals import DescribeObjectsPaginatorName

    data: DescribeObjectsPaginatorName = "describe_objects"
    ```
"""
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = (
    "DescribeObjectsPaginatorName",
    "ListPipelinesPaginatorName",
    "OperatorTypeType",
    "QueryObjectsPaginatorName",
    "TaskStatusType",
)

DescribeObjectsPaginatorName = Literal["describe_objects"]
ListPipelinesPaginatorName = Literal["list_pipelines"]
OperatorTypeType = Literal["BETWEEN", "EQ", "GE", "LE", "REF_EQ"]
QueryObjectsPaginatorName = Literal["query_objects"]
TaskStatusType = Literal["FAILED", "FALSE", "FINISHED"]
