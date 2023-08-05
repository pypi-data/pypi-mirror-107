"""
Type annotations for iotevents service literal definitions.

[Open documentation](./literals.md)

Usage::

    ```python
    from mypy_boto3_iotevents.literals import AnalysisResultLevelType

    data: AnalysisResultLevelType = "ERROR"
    ```
"""
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "AnalysisResultLevelType",
    "AnalysisStatusType",
    "DetectorModelVersionStatusType",
    "EvaluationMethodType",
    "InputStatusType",
    "LoggingLevelType",
    "PayloadTypeType",
)


AnalysisResultLevelType = Literal["ERROR", "INFO", "WARNING"]
AnalysisStatusType = Literal["COMPLETE", "FAILED", "RUNNING"]
DetectorModelVersionStatusType = Literal[
    "ACTIVATING", "ACTIVE", "DEPRECATED", "DRAFT", "FAILED", "INACTIVE", "PAUSED"
]
EvaluationMethodType = Literal["BATCH", "SERIAL"]
InputStatusType = Literal["ACTIVE", "CREATING", "DELETING", "UPDATING"]
LoggingLevelType = Literal["DEBUG", "ERROR", "INFO"]
PayloadTypeType = Literal["JSON", "STRING"]
