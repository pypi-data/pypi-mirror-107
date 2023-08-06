"""
Type annotations for sms-voice service literal definitions.

[Open documentation](./literals.md)

Usage::

    ```python
    from mypy_boto3_sms_voice.literals import EventTypeType

    data: EventTypeType = "ANSWERED"
    ```
"""
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("EventTypeType",)

EventTypeType = Literal[
    "ANSWERED", "BUSY", "COMPLETED_CALL", "FAILED", "INITIATED_CALL", "NO_ANSWER", "RINGING"
]
