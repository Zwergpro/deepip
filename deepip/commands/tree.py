import sys

from deepip.core.views import SimpleView
from deepip.core.builders import build_dep_tree


def tree_command_handler(args):
    root = build_dep_tree()

    if args.package:
        node = root.get_child(args.package)
        if node:
            SimpleView(node, show_version=args.version).show()
            return

        sys.stdout.write(f'There is no package with name: {args.package}\n')
        sys.exit(1)

    SimpleView(root, show_version=args.version).show()


def init_tree_subcommand(subparsers):
    tree = subparsers.add_parser('tree', description='Show dependency tree', help='Show dependency tree')
    tree.set_defaults(func=tree_command_handler)
    tree.add_argument(
        'package',
        nargs='?',
        type=str,
        help='Package name for showing dependencies',
    )

    tree.add_argument(
        '-v',
        '--version',
        action='store_true',
        help='Show package version information',
    )
