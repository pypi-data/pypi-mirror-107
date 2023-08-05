"""
Type annotations for ebs service literal definitions.

[Open documentation](./literals.md)

Usage::

    ```python
    from mypy_boto3_ebs.literals import ChecksumAggregationMethodType

    data: ChecksumAggregationMethodType = "LINEAR"
    ```
"""
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ChecksumAggregationMethodType", "ChecksumAlgorithmType", "StatusType")


ChecksumAggregationMethodType = Literal["LINEAR"]
ChecksumAlgorithmType = Literal["SHA256"]
StatusType = Literal["completed", "error", "pending"]
