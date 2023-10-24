from blockchainetl_common.jobs.exporters.composite_item_exporter import CompositeItemExporter


def blocks_item_exporter(
        blocks_output=None
        , transactions_output=None
    ):
    filename_mapping = {}
    field_mapping = {
        "block": [
            "block_hash",
            "parent_hash",
            "block_number",
            "new_root",
            "block_timestamp",
            "sequencer_address",
            "transaction_count",
            "status"
        ],
        "transaction": [
            "block_number",
            "block_timestamp",
            "block_hash",
            "transaction_hash",
            "_type",
            "version",
            "max_fee",
            "sender_address",
            "contract_class",
            "compiled_class_hash",
            "class_hash",
            "constructor_calldata",
            "contract_address_salt",
            "signature",
            "nonce",
            "contract_address",
            "entry_point_selector",
            "calldata",
            'transaction_index'
        ]
    }

    if blocks_output is not None:
        filename_mapping['block'] = blocks_output

    if transactions_output is not None:
        filename_mapping['transaction'] = transactions_output

    return CompositeItemExporter(
        filename_mapping=filename_mapping,
        field_mapping=field_mapping
    )
