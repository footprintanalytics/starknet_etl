import click

from starknetetl.cli.export_blocks import export_blocks
from starknetetl.cli.export_receipts import export_receipts
from starknetetl.cli.get_block_range_for_timestamps import get_block_range_for_timestamps


@click.group()
@click.version_option(version='1.6.4')
@click.pass_context
def cli(ctx):
    pass


# export
cli.add_command(export_blocks, "export_blocks")
cli.add_command(export_receipts, "export_receipts")

# utils
cli.add_command(get_block_range_for_timestamps, "get_block_range_for_timestamps")
