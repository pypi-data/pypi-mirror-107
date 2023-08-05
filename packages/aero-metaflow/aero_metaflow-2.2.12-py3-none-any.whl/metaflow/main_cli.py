# New file built by Aero Technologies.
# This handles the new "metaflow" input CLI - which currently references S3OP

import click

from .datatools.s3op import create_s3_cli

@click.group(help="Aero's Core commandset")
def cli():
    pass

create_s3_cli(cli)