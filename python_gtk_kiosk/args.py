"""
Argument management module.
"""

import logging

from colorlog import ColoredFormatter

from . import __version__


log = logging.getLogger(__name__)


class InvalidArgument(Exception):
    """
    Custom exception to raise when a command line argument or combination of
    arguments are invalid.
    """


def validate_args(args):
    """
    Validate that arguments are valid.

    :param args: An arguments namespace.
    :type args: :py:class:`argparse.Namespace`

    :return: The validated namespace.
    :rtype: :py:class:`argparse.Namespace`
    """

    logfrmt = (
        '  {thin_white}{asctime}{reset} | '
        '{log_color}{levelname:8}{reset} | '
        '{message}'
    )

    verbosity_levels = {
        0: logging.ERROR,
        1: logging.WARNING,
        2: logging.INFO,
        3: logging.DEBUG,
    }

    stream = logging.StreamHandler()
    stream.setFormatter(ColoredFormatter(fmt=logfrmt, style='{'))

    level = verbosity_levels.get(args.verbosity, logging.DEBUG)
    logging.basicConfig(handlers=[stream], level=level)

    log.debug('Raw arguments:\n{}'.format(args))

    return args


def parse_args(argv=None):
    """
    Argument parsing routine.

    :param list argv: A list of argument strings.

    :return: A parsed and verified arguments namespace.
    :rtype: :py:class:`argparse.Namespace`
    """
    from argparse import ArgumentParser

    parser = ArgumentParser(
        description='Python GTK Kiosk'
    )
    parser.add_argument(
        '-v', '--verbose',
        help='increase verbosity level',
        default=0,
        action='count',
        dest='verbosity',
    )
    parser.add_argument(
        '--version',
        action='version',
        version='{} {}'.format(parser.description, __version__)
    )
    parser.add_argument(
        '-k', '--kiosk',
        help='Enable kiosk mode',
        action='store_true',
    )

    args = parser.parse_args(argv)
    args = validate_args(args)
    return args


__all__ = [
    'parse_args',
]
