"""The main file of the plant module"""
import click
import pendulum

from .target import target


@click.group()
def japscan():
    """
    Heaume japscan provides tools to interact with japscan notification module.
    """


japscan.add_command(target)
