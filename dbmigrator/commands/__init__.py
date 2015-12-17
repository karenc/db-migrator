# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2015, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###

import glob
import os
import sys


__all__ = ('available_commands', 'load_cli')


def available_commands():
    current_directory = os.path.dirname(__file__)
    for path in glob.glob('{}/*.py'.format(current_directory)):
        filename = os.path.basename(path)
        command_name = filename[:-3]
        if not command_name.startswith('_'):
            yield command_name


def _import_attr_n_module(module_name, attr):
    """From the given ``module_name`` import
    the value for ``attr`` (attribute).
    """
    __import__(module_name)
    module = sys.modules[module_name]
    attr = getattr(module, attr)
    return attr, module


def _import_loader(module_name):
    """Given a ``module_name`` import the cli loader."""
    loader, module = _import_attr_n_module(module_name, 'cli_loader')
    return loader, module.__doc__


def load_cli(subparsers):
    """Given a parser, load the CLI subcommands"""
    for command_name in available_commands():
        module = '{}.{}'.format(__package__, command_name)
        loader, description = _import_loader(module)
        parser = subparsers.add_parser(command_name,
                                       help=description)
        command = loader(parser)
        if command is None:
            raise RuntimeError('Failed to load "{}".'.format(command_name))
        parser.set_defaults(cmmd=command)
