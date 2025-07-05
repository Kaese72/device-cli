"""models for device groups."""

import dataclasses
from typing import Any, Dict, List


@dataclasses.dataclass
class Capability:
    """A capability associated with a device group"""

    name: str

    @classmethod
    def from_dict(cls, json: Dict[str, Any]) -> "Capability":
        """Parses a JSON dictionary into an Capability object."""
        return cls(
            name=json["name"],
        )


@dataclasses.dataclass
class Group:
    """A group representing a group of devices."""

    id_: int
    bridge_identifier: str
    bridge_key: str
    name: str = ""
    capabilities: List[Capability] = dataclasses.field(default_factory=list)

    @classmethod
    def from_dict(cls, json: Dict[str, Any]) -> "Group":
        """Parses a JSON dictionary into an Group object."""
        return cls(
            id_=json["id"],
            bridge_identifier=json["bridge-identifier"],
            bridge_key=json["bridge-key"],
            name=json.get("name", ""),
            capabilities=[
                Capability.from_dict(cap) for cap in json.get("capabilities", [])
            ],
        )
