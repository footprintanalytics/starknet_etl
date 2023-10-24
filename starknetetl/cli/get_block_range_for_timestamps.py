import click

from blockchainetl_common.file_utils import smart_open
from blockchainetl_common.thread_local_proxy import ThreadLocalProxy
from starknetetl.rpc.rpc import StarknetRpc
from starknetetl.service.block_range_service import StarknetBlockRangeService

@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-p', '--provider-uri', required=True, type=str, help='The URI of tendermint RPC')
@click.option('-s', '--start-timestamp', required=True, type=int, help='Start unix timestamp, in seconds.')
@click.option('-e', '--end-timestamp', required=True, type=int, help='End unix timestamp, in seconds.')
@click.option('-o', '--output', default='-', show_default=True, type=str, help='The output file. If not specified stdout is used.')
def get_block_range_for_timestamps(provider_uri, start_timestamp, end_timestamp, output):
    """Outputs start and end blocks for given date."""

    service = StarknetBlockRangeService(ThreadLocalProxy(lambda: StarknetRpc(provider_uri)))

    start_block, end_block = service.get_block_range_for_timestamps(start_timestamp, end_timestamp)

    with smart_open(output, 'w') as output_file:
        output_file.write('{},{}\n'.format(start_block, end_block))


# if __name__ == '__main__':
#     get_block_range_for_timestamps('https://starknet-mainnet.g.alchemy.com/v2/2tSCWM-b6JT-Ju4Cbu-ba2bRxStPbGP4', 1688428800, 1688515200, '/Users/pen/cryptoProject/ethereum-etl-airflow/dags/data/starknet/block_range.txt')