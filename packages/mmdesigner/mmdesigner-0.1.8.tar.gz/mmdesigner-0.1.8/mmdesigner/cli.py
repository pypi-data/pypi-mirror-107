import click
import mmdesigner
from mmdesigner import __version__


@click.group()
@click.version_option(__version__, '--version')
def cli():
    pass

