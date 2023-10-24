import click
from blockchainetl_common.file_utils import smart_open

from starknetetl import misc_utils
from starknetetl.jobs.export_receipts_job import ExportReceiptsJob
from starknetetl.jobs.exporters.receipts_item_exporter import receipts_item_exporter
from starknetetl.rpc.rpc import StarknetRpc
from blockchainetl_common.logging_utils import logging_basic_config
from blockchainetl_common.thread_local_proxy import ThreadLocalProxy

logging_basic_config()


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-t', '--transaction-hash', required=True, type=str,
              help='The file containing transaction hashes, one per line.')
@click.option('-p', '--provider-uri',  type=str,
              help='The URI of the remote RPC node')
@click.option('-w', '--max-workers', default=3, type=int, help='The maximum number of workers.')
@click.option('-b', '--batch_size', default=2, type=int, help='The maximum number of batch call.')
@click.option('--receipt_output', default=None, type=str,
              help='The output file for transaction receipt. '
                   'If not provided blocks will not be exported. Use "-" for stdout')
@click.option('--message_output', default=None, type=str,
              help='The output file for message. '
                   'If not provided blocks will not be exported. Use "-" for stdout')
@click.option('--event_output', default=None, type=str,
              help='The output file for event. '
                   'If not provided blocks will not be exported. Use "-" for stdout')
def export_receipts(transaction_hash, provider_uri, max_workers, batch_size,
                    receipt_output, message_output, event_output, token_transfer_output):
    """Export blocks, transactions and actions."""

    if receipt_output is None and message_output is None and event_output is None and token_transfer_output is None:
        raise ValueError(
            'Chain --receipt_output or --message_output or --event_output or --token_transfer_output '
            'options must be provided')
    with smart_open(transaction_hash, 'r') as transaction_block_digests:
        job = ExportReceiptsJob(
            transaction_hash_iterable=transaction_block_digests.read().splitlines(),
            rpc=ThreadLocalProxy(lambda: StarknetRpc(provider_uri)),
            max_workers=max_workers,
            batch_size=batch_size,
            item_exporter=receipts_item_exporter(receipt_output, message_output, event_output, token_transfer_output),
            export_receipts=receipt_output is not None,
            export_messages=message_output is not None,
            export_events=event_output is not None,
            export_token_transfers=token_transfer_output is not None,
        )
    job.run()

#
# if __name__ == '__main__':
#     transaction_hash = 'transactions.txt'
#     misc_utils.extract_field('transactions_2023-07-25-test.json', transaction_hash, 'transaction_hash')
#
#     export_receipts(
#         transaction_hash = transaction_hash,
#         provider_uri='',
#         max_workers=2,batch_size=2,
#         receipt_output = 'receipt_output.json',
#         message_output = 'message_output.json',
#         token_transfer_output = 'token_transfer_output.json',
#         event_output = 'event_output.json'
#     )