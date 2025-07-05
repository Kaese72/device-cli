"""GET from /devices"""

import argparse
import json

from huemie.handle import APIHandle


def argparse_expand(parser: argparse.ArgumentParser):
    parser.set_defaults(func=__adapter_put)
    parser.add_argument(
        "--file",
        type=str,
        required=True,
        help="provide a file with adapter information",
    )
    parser.add_argument(
        "--name",
        type=str,
        required=True,
        help="name of the adapter",
    )
    return parser


def __adapter_put(args: argparse.Namespace):
    handle = APIHandle(args.base_url)
    with open(args.file, "r", encoding="utf-8") as file_handle:
        data = json.load(file_handle)

    handle.put_json(f"adapter-attendant/v0/adapters/{args.name}", data=data)
