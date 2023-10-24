from blockchainetl_common.jobs.exporters.composite_item_exporter import CompositeItemExporter


def receipts_item_exporter(
receipt_output=None, message_output=None, event_output=None, token_transfer_output=None
    ):
    filename_mapping = {}
    field_mapping = {
        "event": [
            'transaction_hash',
            'block_hash',
            'block_number',
            'block_timestamp',
            'data',
            'from_address',
            'keys',
            'event_index'
        ],
        "receipt": [
            'block_number',
            'block_hash',
            'block_timestamp',
            'actual_fee',
            'event_count',
            'messages_sent_count',
            'status',
            'transaction_hash',
            '_type',
            'contract_address'
        ],
        'message': [
            'transaction_hash',
            'block_hash',
            'block_number',
            'block_timestamp',
            'from_address',
            'to_address',
            'payload',
            '_type'
        ],
        'token_transfer': [
            'transaction_hash',
            'block_hash',
            'block_number',
            'block_timestamp',
            'from_address',
            'to_address',
            'contract_address',
            'value',
            'event_index'
        ]
    }

    if receipt_output is not None:
        filename_mapping['receipt'] = receipt_output

    if message_output is not None:
        filename_mapping['message'] = message_output

    if event_output is not None:
        filename_mapping['event'] = event_output

    if token_transfer_output is not None:
        filename_mapping['token_transfer'] = token_transfer_output

    return CompositeItemExporter(
        filename_mapping=filename_mapping,
        field_mapping=field_mapping
    )
