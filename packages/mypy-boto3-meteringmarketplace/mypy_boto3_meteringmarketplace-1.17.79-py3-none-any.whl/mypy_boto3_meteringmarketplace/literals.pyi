"""
Type annotations for meteringmarketplace service literal definitions.

[Open documentation](./literals.md)

Usage::

    ```python
    from mypy_boto3_meteringmarketplace.literals import UsageRecordResultStatusType

    data: UsageRecordResultStatusType = "CustomerNotSubscribed"
    ```
"""
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("UsageRecordResultStatusType",)

UsageRecordResultStatusType = Literal["CustomerNotSubscribed", "DuplicateRecord", "Success"]
