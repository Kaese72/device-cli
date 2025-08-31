"""AttributeAudit model for device attribute change auditing."""

import dataclasses
from datetime import datetime
from typing import Any, Dict


@dataclasses.dataclass
class AttributeAudit:
    id_: int
    device_id: int
    name: str
    timestamp: datetime
    old_boolean_value: bool | None
    old_numeric_value: float | None
    old_text_value: str | None
    new_boolean_value: bool | None
    new_numeric_value: float | None
    new_text_value: str | None

    @classmethod
    def from_dict(cls, json: Dict[str, Any]) -> "AttributeAudit":
        """Parses a JSON dictionary into an AttributeAudit object."""
        return cls(
            id_=json["id"],
            device_id=json["deviceId"],
            name=json["name"],
            timestamp=datetime.fromisoformat(json["timestamp"].replace("Z", "+00:00")),
            old_boolean_value=json["oldBooleanValue"],
            old_numeric_value=json["oldNumericValue"],
            old_text_value=json["oldTextValue"],
            new_boolean_value=json["newBooleanValue"],
            new_numeric_value=json["newNumericValue"],
            new_text_value=json["newTextValue"],
        )

