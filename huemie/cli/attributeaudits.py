"""GET from /device-store/v0/audits/attributes"""

import argparse
from typing import Any, List

import tabulate

from huemie.handle import APIHandle
from huemie.models.attributeaudit import AttributeAudit


def argparse_expand(parser: argparse.ArgumentParser):
    parser.set_defaults(func=__attribute_audits_main)
    parser.add_argument(
        "--device-id",
        type=str,
        dest="device_id",
        help="Filter by device ID",
    )
    parser.add_argument(
        "--attribute",
        type=str,
        dest="attribute_name",
        help="Filter by attribute name",
    )
    parser.add_argument(
        "--since",
        type=str,
        dest="since",
        help="Filter by timestamp (since) on the format 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS'",
    )
    return parser


def __attribute_audits_main(args: argparse.Namespace):
    handle = APIHandle(args.base_url)
    
    # Build query parameters
    queries: List[str] = []
    if args.device_id:
        queries.append(f"deviceId[eq]={args.device_id}")
    if args.attribute_name:
        queries.append(f"name[eq]={args.attribute_name}")
    if args.since:
        queries.append(f"timestamp[gt]={args.since}")
    
    audits = [
        AttributeAudit.from_dict(x)
        for x in handle.get_json("device-store/v0/audits/attributes", queries=queries)
    ]
    
    table: List[List[Any]] = []
    for audit in audits:
        row: List[Any] = [
            audit.id_,
            audit.device_id,
            audit.name,
            audit.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            _format_value(audit.old_boolean_value, audit.old_numeric_value, audit.old_text_value),
            _format_value(audit.new_boolean_value, audit.new_numeric_value, audit.new_text_value),
        ]
        table.append(row)

    print(
        tabulate.tabulate(
            table, 
            headers=["ID", "Device ID", "Attribute", "Timestamp", "Old Value", "New Value"],
        )
    )


def _format_value(bool_val: bool | None, num_val: float | None, text_val: str | None) -> str:
    """Format attribute value based on which type has a meaningful value."""
    if text_val is not None:
        return text_val
    elif num_val is not None:
        return str(num_val)
    elif bool_val is not None:
        return str(bool_val)
    else:
        return ""
