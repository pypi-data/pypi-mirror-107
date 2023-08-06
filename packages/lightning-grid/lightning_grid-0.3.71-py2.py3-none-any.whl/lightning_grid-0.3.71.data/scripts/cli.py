#!python
# Copyright 2020 Grid AI Inc.
"""Entrypoint for the Grid CLI."""
import sys
import traceback

import click
from click import ClickException

import grid.cli as cli
from grid.exceptions import ResourceNotFound
import grid.globals as env
from grid.metadata import __logo__, __version__
from grid.tracking import Segment, TrackingEvents
from grid.utilities import introspect_module

# Referencing from: https://stackoverflow.com/questions/46641928/python-click-multiple-command-names
# Employing a temporary solution since these are only temporary until we fully
# rename them.
ALIASES = {"run": "train", "session": "interactive"}


class AliasedGroup(click.Group):
    def get_command(self, ctx, cmd_name):
        if cmd_name in ALIASES:
            cmd_name = ALIASES[cmd_name]

        return super().get_command(ctx, cmd_name)


@click.group(cls=AliasedGroup)
@click.option(
    '--debug', type=bool, help='Used for logging additional information for debugging purposes.', is_flag=True
)
def main(debug: bool = True) -> None:
    """Grid CLI"""
    if debug:
        env.logger.info('Starting gridrunner in DEGUB mode.')

    env.DEBUG = debug


@main.command()
def version() -> None:
    """
    Prints CLI version to stdout.
    """
    logo = click.style(__logo__, fg='green')
    click.echo(logo)

    version = f"""
                                Grid CLI ({__version__})
                               https://docs.grid.ai
    """
    click.echo(version)


@main.command()
def docs() -> None:
    """
    Open the CLI docs.
    """
    click.launch('https://docs.grid.ai/products/global-cli-configs')


#  Adds all CLI commands. Commands are introspected
#  from the cli module.
for command in introspect_module(cli):
    command: click.Command
    main: click.Group
    main.add_command(command)

if __name__ == '__main__':
    tracker = Segment()
    tracker.send_event(event=TrackingEvents.CLI_STARTED)
    try:
        main.main(prog_name="grid", standalone_mode=False)
        tracker.send_event(event=TrackingEvents.CLI_FINISHED)
    except ClickException as e:
        tracker.report_exception(e)
        e.show()
        sys.exit(e.exit_code)
    except ResourceNotFound as e:
        tracker.report_exception(e)
        tracker.flush()
        print(e)
        sys.exit(2)
    except Exception as e:
        traceback.print_exc()
        tracker.report_exception(e)
        tracker.flush()
        sys.exit(1)
    finally:
        tracker.flush()
