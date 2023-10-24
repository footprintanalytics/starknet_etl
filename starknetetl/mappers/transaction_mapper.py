from starknetetl.domain.transaction import EthTransaction
from starknetetl.utils import hex_to_dec, to_normalized_address


class TransactionMapper:

    def json_dict_to_transaction(self, json_dict, block, transaction_index):
        transaction = EthTransaction()
        transaction.block_hash = block.hash
        transaction.block_number = block.number
        transaction.block_timestamp = block.timestamp

        transaction.transaction_hash = json_dict.get('transaction_hash')
        transaction.type = json_dict.get('type')
        transaction.version = int(str(json_dict.get("version")), 16)
        transaction.max_fee = int(str(json_dict.get("max_fee")), 16) if json_dict.get("max_fee") is not None else None
        transaction.nonce = hex_to_dec(json_dict.get('nonce'))

        transaction.sender_address = to_normalized_address(json_dict.get('sender_address'))
        transaction.contract_address = to_normalized_address(json_dict.get("contract_address"))

        transaction.chain_id = json_dict.get('chain_id')
        transaction.contract_class = json_dict.get('contract_class')
        transaction.compiled_class_hash = json_dict.get('compiled_class_hash')
        transaction.class_hash = json_dict.get("class_hash")
        transaction.constructor_calldata = json_dict.get("constructor_calldata")
        transaction.contract_address_salt = json_dict.get("contract_address_salt")
        transaction.signature = json_dict.get("signature")
        transaction.nonce = int(str(json_dict.get("nonce")), 16) if json_dict.get("nonce") is not None else None
        transaction.entry_point_selector = json_dict.get("entry_point_selector")
        transaction.calldata = json_dict.get("calldata")

        transaction.transaction_index = transaction_index
        return transaction

    def transaction_to_dict(self, transaction):
        return {
            'type': 'transaction',
            'block_number': transaction.block_number,
            'block_timestamp': transaction.block_timestamp,
            'block_hash': transaction.block_hash,
            'transaction_hash': transaction.transaction_hash,
            '_type': transaction.type,
            'version': transaction.version,
            'max_fee': transaction.max_fee,
            'sender_address': transaction.sender_address,
            'chain_id': transaction.chain_id,
            'contract_class': transaction.contract_class,
            'compiled_class_hash': transaction.compiled_class_hash,
            'class_hash': transaction.class_hash,
            "constructor_calldata": transaction.constructor_calldata,
            "contract_address_salt": transaction.contract_address_salt,
            "contract_address": transaction.contract_address,
            "signature": transaction.signature,
            "nonce": transaction.nonce,
            "entry_point_selector": transaction.entry_point_selector,
            "calldata": transaction.calldata,
            "transaction_index": transaction.transaction_index
        }
