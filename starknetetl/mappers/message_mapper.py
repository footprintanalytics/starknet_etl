class MessageMapper:
    def __init__(self, transaction_hash, block_hash, block_number, from_address, to_address, payload, type):
        self.transaction_hash = transaction_hash
        self.block_hash = block_hash
        self.block_number = block_number
        self.from_address = from_address
        self.to_address = to_address
        self.payload = payload
        self.type = type

    @classmethod
    def from_dict(cls, receipt_info, message_info):
        return cls(
            receipt_info["transaction_hash"],
            receipt_info["block_hash"],
            receipt_info["block_number"],
            message_info["from_address"],
            message_info["to_address"],
            message_info["payload"],
            receipt_info["type"]
        )

    def to_dict(self):
        return {
            'type': "message",
            "transaction_hash": self.transaction_hash,
            "block_hash": self.block_hash,
            "block_number": self.block_number,
            "from_address": self.from_address,
            "to_address": self.to_address,
            "payload": self.payload,
            "_type": self.type
        }
