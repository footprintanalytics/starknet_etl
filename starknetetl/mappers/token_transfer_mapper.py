class TokenTransferMapper:
    def __init__(self, transaction_hash, block_hash, block_number, event_index, from_address, to_address, contract_address, value):
        self.transaction_hash = transaction_hash
        self.block_hash = block_hash
        self.block_number = block_number
        self.event_index = event_index
        self.from_address = from_address
        self.to_address = to_address
        self.contract_address = contract_address
        self.value = value

    @classmethod
    def from_dict(cls, event, receipt, event_index):
        return cls(
            receipt["transaction_hash"],
            receipt["block_hash"],
            receipt["block_number"],
            event_index,
            from_address=event['data'][0],
            to_address=event['data'][1],
            contract_address=event["from_address"],
            value=str(int(event['data'][2], 16))
        )

    def to_dict(self):
        return {
            "type": "token_transfer",
            "transaction_hash": self.transaction_hash,
            "block_hash": self.block_hash,
            "block_number": self.block_number,
            "event_index": self.event_index,
            "from_address": self.from_address,
            "to_address": self.to_address,
            "contract_address": self.contract_address,
            "value": self.value
        }