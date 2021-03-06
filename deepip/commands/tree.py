import sys

from deepip.core.api.cache import Cache
from deepip.core.views import SimpleView
from deepip.core.builders import build_dep_tree


def tree_command_handler(args):
    """Handle tree cli command"""
    Cache.init(fake=args.no_cache, path=args.cache_path, expire=args.cache_expire)
    root = build_dep_tree(with_meta=args.latest)
    Cache.dump()

    if args.package:
        node = root.get_child_by_name(args.package)
        if node:
            SimpleView(node, show_version=args.version).show()
            return

        sys.stdout.write(f'There is no package with name: {args.package}\n')
        sys.exit(1)

    SimpleView(root, show_version=args.version).show()


def init_tree_subcommand(subparsers):
    """Init cli parser for tree command"""
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

    tree.add_argument(
        '-l',
        '--latest',
        action='store_true',
        help='Show latest available lib version',
    )

    tree.add_argument(
        '--no-cache',
        dest='no_cache',
        action='store_true',
        help="Don't use cache",
    )

    tree.add_argument(
        '--cache-path',
        dest='cache_path',
        type=Cache.convert_to_cache_file,
        default=None,
        help='Specify cache path',
    )

    tree.add_argument(
        '--cache-expire',
        dest='cache_expire',
        type=int,
        default=None,
        help='Specify cache expire timeout',
    )
