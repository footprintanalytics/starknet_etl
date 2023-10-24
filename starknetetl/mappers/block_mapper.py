import json

from starknetetl.domain.block import EthBlock
from starknetetl.mappers.transaction_mapper import TransactionMapper
from starknetetl.utils import hex_to_dec


class BlockMapper:
    def __init__(self, transaction_mapper=None):
        if transaction_mapper is None:
            self.transaction_mapper = TransactionMapper()
        else:
            self.transaction_mapper = transaction_mapper

    def json_dict_to_block(self, json_dict):
        block = EthBlock()
        origin = json.dumps(json_dict)
        block.number = int(json_dict.get('block_number'))
        block.hash = json_dict.get('block_hash')
        block.parent_hash = json_dict.get('parent_hash')
        block.new_root = json_dict.get('new_root')
        block.timestamp = int(json_dict.get('timestamp'))
        block.status = json_dict.get('status')
        block.sequencer_address = json_dict.get('sequencer_address')

        if 'transactions' in json_dict:
            block.transactions = [
                self.transaction_mapper.json_dict_to_transaction(tx, block, index)
                for index, tx in enumerate(json_dict['transactions'])
                if isinstance(tx, dict)
            ]

            block.transaction_count = len(json_dict['transactions'])
        return block

    def block_to_dict(self, block):
        return {
            'type': 'block',
            'block_number': block.number,
            'block_hash': block.hash,
            'parent_hash': block.parent_hash,
            'new_root': block.new_root,
            'block_timestamp': block.timestamp,
            'sequencer_address': block.sequencer_address,
            'transaction_count': block.transaction_count,
            'status': block.status
        }
