"""Main module for things related to argparse"""

from ntclient.argparser import subparsers as nt_subparsers


def build_subcommands(subparsers):
    """Attaches subcommands to main parser"""
    nt_subparsers.build_init_subcommand(subparsers)
    nt_subparsers.build_nt_subcommand(subparsers)
    nt_subparsers.build_search_subcommand(subparsers)
    nt_subparsers.build_sort_subcommand(subparsers)
    nt_subparsers.build_analyze_subcommand(subparsers)
    nt_subparsers.build_day_subcommand(subparsers)
    nt_subparsers.build_recipe_subcommand(subparsers)
    nt_subparsers.build_biometric_subcommand(subparsers)
