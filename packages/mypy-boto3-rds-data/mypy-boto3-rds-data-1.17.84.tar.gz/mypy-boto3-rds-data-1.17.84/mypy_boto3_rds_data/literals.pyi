"""
Type annotations for rds-data service literal definitions.

[Open documentation](./literals.md)

Usage::

    ```python
    from mypy_boto3_rds_data.literals import DecimalReturnTypeType

    data: DecimalReturnTypeType = "DOUBLE_OR_LONG"
    ```
"""
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("DecimalReturnTypeType", "TypeHintType")

DecimalReturnTypeType = Literal["DOUBLE_OR_LONG", "STRING"]
TypeHintType = Literal["DATE", "DECIMAL", "JSON", "TIME", "TIMESTAMP", "UUID"]
