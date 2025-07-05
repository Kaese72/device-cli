""""""

import dataclasses
from typing import Any, Dict, List, Optional


@dataclasses.dataclass
class Attribute:
    name: str
    numeric_state: Optional[float] = None
    string_state: Optional[str] = None
    boolean_state: Optional[bool] = None

    @classmethod
    def from_dict(cls, json: Dict[str, Any]) -> "Attribute":
        """Parses a JSON dictionary into an Attribute object."""
        return cls(
            name=json["name"],
            numeric_state=json.get("numeric-state"),
            string_state=json.get("string-state"),
            boolean_state=json.get("boolean-state"),
        )


@dataclasses.dataclass
class Capability:
    name: str

    @classmethod
    def from_dict(cls, json: Dict[str, Any]) -> "Capability":
        """Parses a JSON dictionary into an Capability object."""
        return cls(
            name=json["name"],
        )


@dataclasses.dataclass
class Device:
    id_: int
    bridge_identifier: str
    bridge_key: str
    attributes: List[Attribute] = dataclasses.field(default_factory=list)
    capabilities: List[Capability] = dataclasses.field(default_factory=list)

    @classmethod
    def from_dict(cls, json: Dict[str, Any]) -> "Device":
        """Parses a JSON dictionary into an Device object."""
        return cls(
            id_=json["id"],
            attributes=[
                Attribute.from_dict(attr) for attr in json.get("attributes", [])
            ],
            capabilities=[
                Capability.from_dict(cap) for cap in json.get("capabilities", [])
            ],
            bridge_identifier=json["bridge-identifier"],
            bridge_key=json["bridge-key"],
        )

    def get_attribute(self, name: str) -> Optional[Attribute]:
        """Returns the attribute with the given name, or None if it does not exist."""
        for attribute in self.attributes:
            if attribute.name == name:
                return attribute

        return None
