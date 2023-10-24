import click

from starknetetl.jobs.export_blocks_job import ExportBlocksJob
from starknetetl.jobs.exporters.blocks_item_exporter import blocks_item_exporter
from blockchainetl_common.logging_utils import logging_basic_config
from blockchainetl_common.thread_local_proxy import ThreadLocalProxy

from starknetetl.providers.auto import get_provider_from_uri
from starknetetl.service.service import StarknetService

logging_basic_config()


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-s', '--start-block', default=0, type=int, help='Start block')
@click.option('-e', '--end-block', required=True, type=int, help='End block')
@click.option('-p', '--provider-uri', type=str,
              help='The URI of the remote RPC node')
@click.option('-w', '--max-workers', default=3, type=int, help='The maximum number of workers.')
@click.option('-b', '--batch_size', default=2, type=int, help='The maximum number of batch call.')
@click.option('--block_output', default=None, type=str,
              help='The output file for block. '
                   'If not provided blocks will not be exported. Use "-" for stdout')
@click.option('--transaction_output', default=None, type=str,
              help='The output file for transaction. '
                   'If not provided blocks will not be exported. Use "-" for stdout')
def export_blocks_and_transactions(start_block, end_block, provider_uri, max_workers, batch_size, block_output, transaction_output):
    """Export blocks, transactions and actions."""

    if block_output is None and transaction_output is None:
        raise ValueError('Either --block_output or --transaction_output options must be provided')

    job = ExportBlocksJob(
        start_block=start_block,
        end_block=end_block,
        batch_web3_provider=ThreadLocalProxy(lambda: get_provider_from_uri(provider_uri, batch=True)),
        max_workers=max_workers,
        batch_size=batch_size,
        item_exporter=blocks_item_exporter(block_output, transaction_output),
        export_blocks=block_output is not None,
        export_transactions=transaction_output is not None
    )
    job.run()


# if __name__ == '__main__':
#     export_blocks_and_transactions(348754, 348754, '', 1, 1,
#                   'blocks_2023-07-25.json', 'transactions_2023-07-25.json')
