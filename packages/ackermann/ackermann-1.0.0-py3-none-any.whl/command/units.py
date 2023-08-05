"""Starts a david application

Parses commandline arguments and runs the correct command.
"""
import logging
from argparse import ArgumentParser
from typing import List, Dict
from .command import MetaCommand, Command
from .config import config_unit, StopInitException, run


logger = logging.getLogger(__name__)


def _get_log_level(level):
    levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    level = levels[min(len(levels)-1, level)]
    return level

def _set_log_level(level):
    logging.basicConfig(level=_get_log_level(level))


@config_unit
def init_arg_parser(config):
    parser = ArgumentParser(prog=config.get("PROJECT_NAME", "TODO"), add_help=False)
    parser.add_argument(
        "-h",
        "--help",
        action="store_true",
        help="show this help message and exit",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="raise log level",
    )

    parser.add_argument('-c', '--config', help='Config file')
    known_args, _ = parser.parse_known_args()
    _set_log_level(known_args.verbose)

    # Store known args for help
    config["ARGS"] = known_args

    if known_args.config:
        config.add_target(parse_config)

    config["ARG_PARSER"] = parser

    subparsers = parser.add_subparsers(
        required=True,
        dest="command",
        title="Command",
        description="Which command to run",
        help="",
    )
    config["ARG_COMMAND_PARSER"] = subparsers


@config_unit(depends=init_arg_parser, after=init_arg_parser)
def init_arg_subparser(config):
    subparsers = config["ARG_COMMAND_PARSER"]
    for name, command in MetaCommand.commands.items():
        logger.debug("Adds Command %s", name)
        subparser = subparsers.add_parser(name, help=command.short_description)
        command.get_arguments(subparser)


# TODO add after
@config_unit(depends=init_arg_parser, before=init_arg_subparser)
def parse_config(config):
    from importlib import import_module
    filename = config["ARGS"].config

    try:
        module = import_module(filename)
    except ModuleNotFoundError as e:
        logger.debug("Importing config threw exception", exc_info=e)
        # TODO why?
        import importlib.util
        spec = importlib.util.spec_from_file_location("base_config", filename)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

    for key in dir(module):
        if key.startswith("__") and key.endswith("__"):
            continue
        value = getattr(module, key)
        config[key] = value


@config_unit(depends=init_arg_parser, after=[init_arg_subparser, init_arg_parser, parse_config])
def parse_parameters(config):
    config["ARGS"] = config["ARG_PARSER"].parse_args()

    if config["ARGS"].help:
        config["ARG_PARSER"].print_help()
        raise StopInitException()

    _set_log_level(config["ARGS"].verbose)


@config_unit(
    depends=[
        parse_parameters,
        init_arg_subparser,
    ],
    after=[
        parse_config,
        parse_parameters,
        init_arg_subparser,
    ]
)
def run_command(config):
    command_cls = MetaCommand.commands[config["ARGS"].command]
    command = command_cls()
    config.add_targets(command.targets)

    if command.is_async:
        config.set_func(command.async_run)
    else:
        config.set_func(command.run)


@config_unit(after=[init_arg_parser])
def systemd_logging_integration(config):
    if "DISABLE_SYSTEMD_LOGGING" in config and config["DISABLE_SYSTEMD_LOGGING"]:
        return

    from systemd.journal import JournalHandler

    journald_handler = JournalHandler()
    root_logger = logging.root
    # TODO
    root_logger.removeHandler(root_logger.handlers[0])
    root_logger.addHandler(journald_handler)
    root_logger.setLevel(_get_log_level(config["ARGS"].verbose))
    config["SYSTEMD"] = True
    logger.info("Enabled systemd logging")


def main():
    run(targets=[run_command])
