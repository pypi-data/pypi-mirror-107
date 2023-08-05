"""The main file of the plant module"""
import click
import pendulum

from .ls import ls
from .status import status


@click.group()
def plant():
    """
    Heaume plant provides information about my plants.
    """


plant.add_command(status)
plant.add_command(ls)
