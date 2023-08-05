import yaml

from miniff import __version__
from miniff.ml_util import exec_workflows
from miniff.units import init_default_atomic_units, new_units_context
from miniff.util import default_logger

import argparse
from collections import OrderedDict
import logging


def ordered_load(stream):
    class OrderedLoader(yaml.SafeLoader):
        pass

    def construct_mapping(_loader, _node):
        _loader.flatten_mapping(_node)
        return OrderedDict(_loader.construct_pairs(_node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.load(stream, OrderedLoader)


class RepeatingArgAction(argparse.Action):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.values = 0

    def __call__(self, parser, args, values, option_string=None):
        if values is None:
            self.values += 1
        else:
            try:
                self.values = int(values)
            except ValueError:
                self.values = values.count('v') + 1
        setattr(args, self.dest, self.values)


parser = argparse.ArgumentParser(prog="miniff", description="Run miniff workflow")
parser.add_argument("-v", "--verbose", action=RepeatingArgAction, help="Verbose output", nargs="?")
parser.add_argument("file", help="file with the workflow", metavar="YAML")

options = parser.parse_args()

if options.file == "version":
    print(__version__)

else:
    logger = default_logger(lvl={1: logging.INFO, 2: logging.DEBUG}.get(options.verbose, logging.WARNING))
    logger.info(f"miniff {__version__}")

    with new_units_context():  # in case __main__ is imported from elsewhere
        init_default_atomic_units()
        with open(options.file, 'r') as f:
            exec_workflows(ordered_load(f), log=logger)
