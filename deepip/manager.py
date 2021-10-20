import argparse

import pkg_resources

from deepip.main import print_dep_tree, print_dep_tree_for_package


def tree_command_helper(args):
    if args.package:
        print_dep_tree_for_package(args.package)
        return

    print_dep_tree()


def init_main_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='deepip', description='Deepip command line tool')
    parser.add_argument(
        '-v',
        '--version',
        action='store_true',
        help='Show lib version',
    )

    subparsers = parser.add_subparsers(title='commands', dest='command')

    tree = subparsers.add_parser('tree', description='Show dependency tree', help='Show dependency tree')
    tree.set_defaults(func=tree_command_helper)
    tree.add_argument(
        'package',
        nargs='?',
        type=str,
        help='Package name for showing dependencies',
    )

    return parser


def process_command_line():
    parser = init_main_parser()
    args = parser.parse_args()

    if args.version:
        version = pkg_resources.working_set.by_key['deepip'].version
        print(f'deepip {version}')
        return

    if not args.command:
        print('hello')
        return

    if args.func:
        args.func(args)
