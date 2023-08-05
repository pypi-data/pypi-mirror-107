"""
Type annotations for pi service literal definitions.

[Open documentation](./literals.md)

Usage::

    ```python
    from mypy_boto3_pi.literals import ServiceTypeType

    data: ServiceTypeType = "RDS"
    ```
"""
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ServiceTypeType",)


ServiceTypeType = Literal["RDS"]
