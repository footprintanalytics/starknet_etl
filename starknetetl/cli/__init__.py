import click

from starknetetl.cli.export_blocks_and_transactions import export_blocks_and_transactions
from starknetetl.cli.export_receipts import export_receipts
from starknetetl.cli.stream import stream


@click.group()
@click.version_option(version='1.6.4')
@click.pass_context
def cli(ctx):
    pass


# export
cli.add_command(export_blocks_and_transactions, "export_blocks")
cli.add_command(export_receipts, "export_receipts")
cli.add_command(stream, "stream")

# utils
# cli.add_command(get_block_range_for_timestamps, "get_block_range_for_timestamps")
