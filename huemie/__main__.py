"""Script file for huemie device cli"""

import argparse
import huemie.cli.devicesget
import huemie.cli.devicecapabilitytrigger
import huemie.cli.groupcapabilitytrigger
import huemie.cli.groupsget
import huemie.cli.adapterput

PARSER = argparse.ArgumentParser(description="Huemie device cli")
PARSER.add_argument(
    "--base-url", type=str, dest="base_url", default="http://app.huemie.space"
)
MAIN_SUB = PARSER.add_subparsers(required=True)

# Devices
DEVICES_PARSER = MAIN_SUB.add_parser("devices")
DEVICES_SUB = DEVICES_PARSER.add_subparsers(required=True)
huemie.cli.devicesget.argparse_expand(DEVICES_SUB.add_parser("get"))
huemie.cli.devicecapabilitytrigger.argparse_expand(DEVICES_SUB.add_parser("trigger"))
# Groups
GROUPS_PARSER = MAIN_SUB.add_parser("groups")
GROUPS_SUB = GROUPS_PARSER.add_subparsers(required=True)
huemie.cli.groupsget.argparse_expand(GROUPS_SUB.add_parser("get"))
huemie.cli.groupcapabilitytrigger.argparse_expand(GROUPS_SUB.add_parser("trigger"))
# Adapter attendant
ADAPTERS_PARSER = MAIN_SUB.add_parser("adapters")
ADAPTERS_SUB = ADAPTERS_PARSER.add_subparsers(required=True)
huemie.cli.adapterput.argparse_expand(ADAPTERS_SUB.add_parser("update"))

# Parse and run
ARGS = PARSER.parse_args()
ARGS.func(ARGS)
