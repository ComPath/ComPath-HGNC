# -*- coding: utf-8 -*-

import logging

import click
from bio2bel.constants import DEFAULT_CACHE_CONNECTION

from .manager import Manager

log = logging.getLogger(__name__)


def set_debug(level):
    logging.basicConfig(level=level, format="%(asctime)s - %(levelname)s - %(message)s")


def set_debug_param(debug):
    if debug == 1:
        set_debug(20)
    elif debug == 2:
        set_debug(10)


@click.group()
@click.option('-c', '--connection', help='Defaults to {}'.format(DEFAULT_CACHE_CONNECTION))
@click.pass_context
def main(ctx, connection):
    """Load ComPath HGNC"""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    ctx.obj = Manager(connection=connection)


@main.command()
@click.option('-v', '--debug', count=True, help="Turn on debugging.")
@click.pass_obj
def populate(manager, debug):
    """Populate the database"""
    set_debug_param(debug)
    manager.create_all()
    manager.populate()


@main.command()
@click.option('-v', '--debug', count=True, help="Turn on debugging.")
@click.option('-y', '--yes', is_flag=True, help="Automatically answer yes")
@click.pass_obj
def drop(manager, debug, yes):
    """Drops the database"""
    set_debug_param(debug)
    if yes or click.confirm('Do you really want to delete the database?'):
        manager.drop_all()


if __name__ == '__main__':
    main()
