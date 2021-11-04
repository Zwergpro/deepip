import argparse
import sys

import pkg_resources

from deepip.commands.tree import init_tree_subcommand


def init_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='deepip', description='Deepip command line tool')
    parser.add_argument('-V', dest='lib_version', action='store_true', help='Show lib version')
    subparsers = parser.add_subparsers(title='commands', dest='command')

    init_tree_subcommand(subparsers)

    return parser


def process_command_line():
    parser = init_parser()
    args = parser.parse_args()

    if args.lib_version:
        version = pkg_resources.working_set.by_key['deepip'].version
        sys.stdout.write(f'deepip {version}\n')
        return

    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)
