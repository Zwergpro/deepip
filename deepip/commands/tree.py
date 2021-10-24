from deepip.main import print_dep_tree_for_package, print_dep_tree_v2


def tree_command_handler(args):
    if args.package:
        print_dep_tree_for_package(args.package)
        return

    print_dep_tree_v2()


def init_tree_subcommand(subparsers):
    tree = subparsers.add_parser('tree', description='Show dependency tree', help='Show dependency tree')
    tree.set_defaults(func=tree_command_handler)
    tree.add_argument(
        'package',
        nargs='?',
        type=str,
        help='Package name for showing dependencies',
    )
