class TransactionMapper:
    def __init__(self, block_number, block_hash, block_timestamp, transaction_hash, type, version, max_fee, sender_address,
                 chain_id, contract_class, compiled_class_hash, class_hash, constructor_calldata, contract_address_salt,
                 signature, nonce, contract_address, entry_point_selector, calldata, transaction_index):
        self.block_number = block_number
        self.block_hash = block_hash
        self.block_timestamp = block_timestamp
        self.transaction_hash = transaction_hash
        self.type = type
        self.version = version
        self.max_fee = max_fee
        self.sender_address = sender_address
        self.chain_id = chain_id
        self.contract_class = contract_class
        self.compiled_class_hash = compiled_class_hash
        self.class_hash = class_hash
        self.constructor_calldata = constructor_calldata
        self.contract_address_salt = contract_address_salt
        self.signature = signature
        self.nonce = nonce
        self.contract_address = contract_address
        self.entry_point_selector = entry_point_selector
        self.calldata = calldata
        self.transaction_index = transaction_index

    @classmethod
    def from_dict(cls, transaction, block, transaction_index):
        try:
            return cls(
                block["block_number"],
                block['block_hash'],
                block["timestamp"],
                transaction["transaction_hash"],
                transaction["type"],
                int(str(transaction["version"]), 16),
                int(str(transaction.get("max_fee")), 16) if transaction.get("max_fee") is not None else None,
                transaction.get("sender_address"),
                transaction.get("chain_id"),
                transaction.get("contract_class"),
                transaction.get("compiled_class_hash"),
                transaction.get("class_hash"),
                transaction.get("constructor_calldata"),
                transaction.get("contract_address_salt"),
                transaction.get("signature"),
                int(str(transaction.get("nonce")), 16) if transaction.get("nonce") is not None else None,
                transaction.get("contract_address"),
                transaction.get("entry_point_selector"),
                transaction.get("calldata"),
                transaction_index
            )
        except Exception as e:
            print(transaction)
            raise e

    def to_dict(self):
        return {
            'type': 'transaction',
            "block_number": self.block_number,
            "block_timestamp": self.block_timestamp,
            "block_hash": self.block_hash,
            "transaction_hash": self.transaction_hash,
            "_type": self.type,
            "version": self.version,
            "max_fee": self.max_fee,
            "sender_address": self.sender_address,
            "chain_id": self.chain_id,
            "contract_class": self.contract_class,
            "compiled_class_hash": self.compiled_class_hash,
            "class_hash": self.class_hash,
            "constructor_calldata": self.constructor_calldata,
            "contract_address_salt": self.contract_address_salt,
            "signature": self.signature,
            "nonce": self.nonce,
            "contract_address": self.contract_address,
            "entry_point_selector": self.entry_point_selector,
            "calldata": self.calldata,
            "transaction_index": self.transaction_index
        }
