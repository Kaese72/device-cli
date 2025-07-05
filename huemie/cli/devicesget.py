"""GET from /devices"""

import argparse
from typing import Any, List, Set

import tabulate

from huemie.handle import APIHandle
from huemie.models.device import Device


def argparse_expand(parser: argparse.ArgumentParser):
    parser.set_defaults(func=__devices_get_main)
    parser.add_argument(
        "--filter",
        type=str,
        dest="filters",
        action="append",
        default=[],
        help="provide a filter on the format attribute[operator]=value",
    )
    return parser


def __devices_get_main(args: argparse.Namespace):
    handle = APIHandle(args.base_url)
    devices = [
        Device.from_dict(x)
        for x in handle.get_json("device-store/v0/devices", queries=args.filters)
    ]
    attribute_names_s: Set[str] = set()
    for device in devices:
        for attribute in device.attributes:
            attribute_names_s.add(attribute.name)

    attribute_names_s.remove("description")
    attribute_names_l = ["description"] + sorted(list(attribute_names_s))
    table: List[List[Any]] = []
    for device in devices:
        row: List[Any] = [device.id_]
        for attribute_name in attribute_names_l:
            d_attribute = device.get_attribute(attribute_name)
            if d_attribute is not None:
                if d_attribute.numeric_state is not None:
                    row.append(d_attribute.numeric_state)
                elif d_attribute.string_state is not None:
                    row.append(d_attribute.string_state)
                elif d_attribute.boolean_state is not None:
                    row.append(d_attribute.boolean_state)
                else:
                    row.append("?")
            else:
                row.append("")

        # Add capability names
        row.append(
            ", ".join(sorted([capability.name for capability in device.capabilities]))
        )

        table.append(row)

    print(
        tabulate.tabulate(
            table, headers=["id"] + list(attribute_names_l) + ["capabilities"]
        )
    )
