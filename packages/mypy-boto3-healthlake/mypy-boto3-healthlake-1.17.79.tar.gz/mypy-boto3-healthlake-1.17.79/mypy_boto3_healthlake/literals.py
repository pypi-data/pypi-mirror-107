"""
Type annotations for healthlake service literal definitions.

[Open documentation](./literals.md)

Usage::

    ```python
    from mypy_boto3_healthlake.literals import DatastoreStatusType

    data: DatastoreStatusType = "ACTIVE"
    ```
"""
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("DatastoreStatusType", "FHIRVersionType", "JobStatusType", "PreloadDataTypeType")


DatastoreStatusType = Literal["ACTIVE", "CREATING", "DELETED", "DELETING"]
FHIRVersionType = Literal["R4"]
JobStatusType = Literal["COMPLETED", "FAILED", "IN_PROGRESS", "SUBMITTED"]
PreloadDataTypeType = Literal["SYNTHEA"]
