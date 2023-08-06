"""
Type annotations for iotdeviceadvisor service literal definitions.

[Open documentation](./literals.md)

Usage::

    ```python
    from mypy_boto3_iotdeviceadvisor.literals import StatusType

    data: StatusType = "CANCELED"
    ```
"""
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("StatusType", "SuiteRunStatusType")


StatusType = Literal[
    "CANCELED",
    "ERROR",
    "FAIL",
    "PASS",
    "PASS_WITH_WARNINGS",
    "PENDING",
    "RUNNING",
    "STOPPED",
    "STOPPING",
]
SuiteRunStatusType = Literal[
    "CANCELED",
    "ERROR",
    "FAIL",
    "PASS",
    "PASS_WITH_WARNINGS",
    "PENDING",
    "RUNNING",
    "STOPPED",
    "STOPPING",
]
