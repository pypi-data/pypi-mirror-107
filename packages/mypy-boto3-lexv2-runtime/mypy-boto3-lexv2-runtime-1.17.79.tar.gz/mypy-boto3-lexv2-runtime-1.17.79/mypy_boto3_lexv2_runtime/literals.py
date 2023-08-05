"""
Type annotations for lexv2-runtime service literal definitions.

[Open documentation](./literals.md)

Usage::

    ```python
    from mypy_boto3_lexv2_runtime.literals import ConfirmationStateType

    data: ConfirmationStateType = "Confirmed"
    ```
"""
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "ConfirmationStateType",
    "DialogActionTypeType",
    "IntentStateType",
    "MessageContentTypeType",
    "SentimentTypeType",
)


ConfirmationStateType = Literal["Confirmed", "Denied", "None"]
DialogActionTypeType = Literal["Close", "ConfirmIntent", "Delegate", "ElicitIntent", "ElicitSlot"]
IntentStateType = Literal["Failed", "Fulfilled", "InProgress", "ReadyForFulfillment", "Waiting"]
MessageContentTypeType = Literal["CustomPayload", "ImageResponseCard", "PlainText", "SSML"]
SentimentTypeType = Literal["MIXED", "NEGATIVE", "NEUTRAL", "POSITIVE"]
