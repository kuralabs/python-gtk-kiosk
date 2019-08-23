"""
python_gtk_kiosk executable module entry point.
"""

from sys import exit
from os import getuid, getpid
from logging import getLogger as get_logger

from setproctitle import setproctitle

from . import __version__
from .args import parse_args, InvalidArgument


log = get_logger(__name__)


def main():
    """
    Application main function.
    """

    # Parse arguments
    try:
        args = parse_args()
    except InvalidArgument as e:
        log.error(e)
        return -1

    # Log startup information
    setproctitle('python-gtk-kiosk')

    log.info('Starting App UI {}'.format(__version__))
    log.info('Started by user UID {} using PID {}'.format(
        getuid(),
        getpid(),
    ))

    # Instance and start the UI
    log.info('Importing UI module ...')
    from .ui import AppUI

    # Create applications objects
    log.info('Creating UI ...')
    ui = AppUI(args.kiosk)

    # Start UI
    log.info('Starting UI ...')
    ui.start()

    return 0


if __name__ == '__main__':
    exit(main())


__all__ = [
    'main',
]
