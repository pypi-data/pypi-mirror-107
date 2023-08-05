#!/usr/bin/env python

"""The main file of the Heaume CLI"""
import click
import pendulum

from heaume_cli.commands.plant import plant
from heaume_cli.commands.japscan import japscan


@click.group()
def heaume():
    """
    Heaume is a CLI that provides helper for Dylan Do Amaral.

    Use 'heaume' to start
    """


heaume.add_command(plant)
heaume.add_command(japscan)
heaume()
