"""GET from /devices"""

import argparse
from typing import Any, Dict, Union

from huemie.handle import APIHandle


def argparse_expand(parser: argparse.ArgumentParser):
    parser.set_defaults(func=__devices_capability_trigger_main)
    parser.add_argument("--device", type=str, help="The device id", required=True)
    parser.add_argument(
        "--capability", type=str, help="The capability name", required=True
    )
    parser.add_argument(
        "--arg",
        type=str,
        nargs="*",
        help=(
            "A string argument on the format 'key(?:type)=value'."
            "The optional type is needed when the value can not be sniffed"
        ),
    )
    return parser


def __devices_capability_trigger_main(args: argparse.Namespace):
    handle = APIHandle(args.base_url)
    arguments: Dict[str, Any] = {}
    argument: str
    for argument in args.arg or []:
        assert isinstance(argument, str)
        value: Union[str, float, bool]
        assert "=" in argument, f"Could not separate argument, '{argument}'"
        key, value = argument.split("=", 1)
        if ":" in key:
            key, type_ = key.split(":", 1)
            if type_ == "float":
                value = float(value)
            elif type_ == "bool":
                value = value.lower() in ["true", "1"]
            elif type_ == "str":
                pass
            else:
                raise ValueError(f"Unknown type '{type_}'")

        arguments[key] = value

    handle.post_json(
        path=f"device-store/v0/devices/{args.device}/capabilities/{args.capability}",
        data=arguments,
    )
