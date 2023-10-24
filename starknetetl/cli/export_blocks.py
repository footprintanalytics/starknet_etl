import click

from starknetetl.jobs.export_blocks_job import ExportBlocksJob
from starknetetl.jobs.exporters.blocks_item_exporter import blocks_item_exporter
from starknetetl.rpc.rpc import StarknetRpc
from blockchainetl_common.logging_utils import logging_basic_config
from blockchainetl_common.thread_local_proxy import ThreadLocalProxy

logging_basic_config()


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-s', '--start-block', default=0, type=int, help='Start block')
@click.option('-e', '--end-block', required=True, type=int, help='End block')
@click.option('-p', '--provider-uri',  type=str,
              help='The URI of the remote RPC node')
@click.option('-w', '--max-workers', default=3, type=int, help='The maximum number of workers.')
@click.option('-b', '--batch_size', default=2, type=int, help='The maximum number of batch call.')
@click.option('--block_output', default=None, type=str,
              help='The output file for block. '
                   'If not provided blocks will not be exported. Use "-" for stdout')
@click.option('--transaction_output', default=None, type=str,
              help='The output file for transaction. '
                   'If not provided blocks will not be exported. Use "-" for stdout')
def export_blocks(start_block, end_block, provider_uri, max_workers, batch_size, block_output, transaction_output):
    """Export blocks, transactions and actions."""

    if block_output is None and transaction_output is None:
        raise ValueError('Chain --block_output or --transaction_output options must be provided')

    job = ExportBlocksJob(
        start_block=start_block,
        end_block=end_block,
        rpc=ThreadLocalProxy(lambda: StarknetRpc(provider_uri)),
        max_workers=max_workers,
        batch_size=batch_size,
        item_exporter=blocks_item_exporter(block_output, transaction_output),
        export_blocks=block_output is not None,
        export_transactions=transaction_output is not None
    )
    job.run()


# if __name__ == '__main__':
#     export_blocks(96872, 97776, 'https://starknet-mainnet.g.alchemy.com/v2/2tSCWM-b6JT-Ju4Cbu-ba2bRxStPbGP4', 2,2,
#                   '/Users/pen/cryptoProject/ethereum-etl-airflow/dags/data/starknet/blocks_2023-07-25.json',
#                   '/Users/pen/cryptoProject/ethereum-etl-airflow/dags/data/starknet/transactions_2023-07-25.json',
#                   )
