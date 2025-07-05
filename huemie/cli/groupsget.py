"""GET from /devices"""

import argparse
import pprint
from typing import Any, List, Set

import tabulate

from huemie.handle import APIHandle
from huemie.models.group import Group


def argparse_expand(parser: argparse.ArgumentParser):
    parser.set_defaults(func=__groups_get_main)
    parser.add_argument(
        "--filter",
        type=str,
        dest="filters",
        action="append",
        default=[],
        help="provide a filter on the format attribute[operator]=value",
    )
    return parser


def __groups_get_main(args: argparse.Namespace):
    handle = APIHandle(args.base_url)
    groups = [
        Group.from_dict(x)
        for x in handle.get_json("device-store/v0/groups", queries=args.filters)
    ]

    table: List[List[Any]] = []
    for group in groups:
        table.append(
            [group.id_, group.name, ", ".join([x.name for x in group.capabilities])]
        )

    print(tabulate.tabulate(table, headers=["id", "name", "capabilities"]))
