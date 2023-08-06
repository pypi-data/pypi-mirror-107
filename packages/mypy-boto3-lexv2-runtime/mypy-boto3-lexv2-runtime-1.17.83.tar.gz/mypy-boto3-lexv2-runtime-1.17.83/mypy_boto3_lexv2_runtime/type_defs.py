"""
Type annotations for lexv2-runtime service type definitions.

[Open documentation](./type_defs.md)

Usage::

    ```python
    from mypy_boto3_lexv2_runtime.type_defs import ActiveContextTimeToLiveTypeDef

    data: ActiveContextTimeToLiveTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List

from botocore.response import StreamingBody

from .literals import (
    ConfirmationStateType,
    DialogActionTypeType,
    IntentStateType,
    MessageContentTypeType,
    SentimentTypeType,
)

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ActiveContextTimeToLiveTypeDef",
    "ActiveContextTypeDef",
    "ButtonTypeDef",
    "ConfidenceScoreTypeDef",
    "DeleteSessionResponseTypeDef",
    "DialogActionTypeDef",
    "GetSessionResponseTypeDef",
    "ImageResponseCardTypeDef",
    "IntentTypeDef",
    "InterpretationTypeDef",
    "MessageTypeDef",
    "PutSessionResponseTypeDef",
    "RecognizeTextResponseTypeDef",
    "RecognizeUtteranceResponseTypeDef",
    "SentimentResponseTypeDef",
    "SentimentScoreTypeDef",
    "SessionStateTypeDef",
    "SlotTypeDef",
    "ValueTypeDef",
)

ActiveContextTimeToLiveTypeDef = TypedDict(
    "ActiveContextTimeToLiveTypeDef",
    {
        "timeToLiveInSeconds": int,
        "turnsToLive": int,
    },
)

_RequiredActiveContextTypeDef = TypedDict(
    "_RequiredActiveContextTypeDef",
    {
        "name": str,
        "timeToLive": "ActiveContextTimeToLiveTypeDef",
    },
)
_OptionalActiveContextTypeDef = TypedDict(
    "_OptionalActiveContextTypeDef",
    {
        "contextAttributes": Dict[str, str],
    },
    total=False,
)


class ActiveContextTypeDef(_RequiredActiveContextTypeDef, _OptionalActiveContextTypeDef):
    pass


ButtonTypeDef = TypedDict(
    "ButtonTypeDef",
    {
        "text": str,
        "value": str,
    },
)

ConfidenceScoreTypeDef = TypedDict(
    "ConfidenceScoreTypeDef",
    {
        "score": float,
    },
    total=False,
)

DeleteSessionResponseTypeDef = TypedDict(
    "DeleteSessionResponseTypeDef",
    {
        "botId": str,
        "botAliasId": str,
        "localeId": str,
        "sessionId": str,
    },
    total=False,
)

_RequiredDialogActionTypeDef = TypedDict(
    "_RequiredDialogActionTypeDef",
    {
        "type": DialogActionTypeType,
    },
)
_OptionalDialogActionTypeDef = TypedDict(
    "_OptionalDialogActionTypeDef",
    {
        "slotToElicit": str,
    },
    total=False,
)


class DialogActionTypeDef(_RequiredDialogActionTypeDef, _OptionalDialogActionTypeDef):
    pass


GetSessionResponseTypeDef = TypedDict(
    "GetSessionResponseTypeDef",
    {
        "sessionId": str,
        "messages": List["MessageTypeDef"],
        "interpretations": List["InterpretationTypeDef"],
        "sessionState": "SessionStateTypeDef",
    },
    total=False,
)

_RequiredImageResponseCardTypeDef = TypedDict(
    "_RequiredImageResponseCardTypeDef",
    {
        "title": str,
    },
)
_OptionalImageResponseCardTypeDef = TypedDict(
    "_OptionalImageResponseCardTypeDef",
    {
        "subtitle": str,
        "imageUrl": str,
        "buttons": List["ButtonTypeDef"],
    },
    total=False,
)


class ImageResponseCardTypeDef(
    _RequiredImageResponseCardTypeDef, _OptionalImageResponseCardTypeDef
):
    pass


_RequiredIntentTypeDef = TypedDict(
    "_RequiredIntentTypeDef",
    {
        "name": str,
    },
)
_OptionalIntentTypeDef = TypedDict(
    "_OptionalIntentTypeDef",
    {
        "slots": Dict[str, "SlotTypeDef"],
        "state": IntentStateType,
        "confirmationState": ConfirmationStateType,
    },
    total=False,
)


class IntentTypeDef(_RequiredIntentTypeDef, _OptionalIntentTypeDef):
    pass


InterpretationTypeDef = TypedDict(
    "InterpretationTypeDef",
    {
        "nluConfidence": "ConfidenceScoreTypeDef",
        "sentimentResponse": "SentimentResponseTypeDef",
        "intent": "IntentTypeDef",
    },
    total=False,
)

MessageTypeDef = TypedDict(
    "MessageTypeDef",
    {
        "content": str,
        "contentType": MessageContentTypeType,
        "imageResponseCard": "ImageResponseCardTypeDef",
    },
    total=False,
)

PutSessionResponseTypeDef = TypedDict(
    "PutSessionResponseTypeDef",
    {
        "contentType": str,
        "messages": str,
        "sessionState": str,
        "requestAttributes": str,
        "sessionId": str,
        "audioStream": StreamingBody,
    },
    total=False,
)

RecognizeTextResponseTypeDef = TypedDict(
    "RecognizeTextResponseTypeDef",
    {
        "messages": List["MessageTypeDef"],
        "sessionState": "SessionStateTypeDef",
        "interpretations": List["InterpretationTypeDef"],
        "requestAttributes": Dict[str, str],
        "sessionId": str,
    },
    total=False,
)

RecognizeUtteranceResponseTypeDef = TypedDict(
    "RecognizeUtteranceResponseTypeDef",
    {
        "inputMode": str,
        "contentType": str,
        "messages": str,
        "interpretations": str,
        "sessionState": str,
        "requestAttributes": str,
        "sessionId": str,
        "inputTranscript": str,
        "audioStream": StreamingBody,
    },
    total=False,
)

SentimentResponseTypeDef = TypedDict(
    "SentimentResponseTypeDef",
    {
        "sentiment": SentimentTypeType,
        "sentimentScore": "SentimentScoreTypeDef",
    },
    total=False,
)

SentimentScoreTypeDef = TypedDict(
    "SentimentScoreTypeDef",
    {
        "positive": float,
        "negative": float,
        "neutral": float,
        "mixed": float,
    },
    total=False,
)

SessionStateTypeDef = TypedDict(
    "SessionStateTypeDef",
    {
        "dialogAction": "DialogActionTypeDef",
        "intent": "IntentTypeDef",
        "activeContexts": List["ActiveContextTypeDef"],
        "sessionAttributes": Dict[str, str],
        "originatingRequestId": str,
    },
    total=False,
)

SlotTypeDef = TypedDict(
    "SlotTypeDef",
    {
        "value": "ValueTypeDef",
    },
    total=False,
)

_RequiredValueTypeDef = TypedDict(
    "_RequiredValueTypeDef",
    {
        "interpretedValue": str,
    },
)
_OptionalValueTypeDef = TypedDict(
    "_OptionalValueTypeDef",
    {
        "originalValue": str,
        "resolvedValues": List[str],
    },
    total=False,
)


class ValueTypeDef(_RequiredValueTypeDef, _OptionalValueTypeDef):
    pass
