"""
Type annotations for kinesisanalytics service literal definitions.

[Open documentation](./literals.md)

Usage::

    ```python
    from mypy_boto3_kinesisanalytics.literals import ApplicationStatusType

    data: ApplicationStatusType = "DELETING"
    ```
"""
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ApplicationStatusType", "InputStartingPositionType", "RecordFormatTypeType")


ApplicationStatusType = Literal["DELETING", "READY", "RUNNING", "STARTING", "STOPPING", "UPDATING"]
InputStartingPositionType = Literal["LAST_STOPPED_POINT", "NOW", "TRIM_HORIZON"]
RecordFormatTypeType = Literal["CSV", "JSON"]
