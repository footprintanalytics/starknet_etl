class EventMapper:
    def __init__(self, transaction_hash, block_hash, block_number,
                data, from_address, keys, event_index):
        self.transaction_hash = transaction_hash
        self.block_hash = block_hash
        self.block_number = block_number
        self.data = data
        self.from_address = from_address
        self.keys = keys
        self.event_index = event_index

    @classmethod
    def from_dict(cls, event, receipt, event_index):
        return cls(
            receipt["transaction_hash"],
            receipt["block_hash"],
            receipt["block_number"],
            event["data"],
            event["from_address"],
            event["keys"],
            event_index
        )

    def to_dict(self):
        return {
            'type': 'event',
            "transaction_hash": self.transaction_hash,
            "block_hash": self.block_hash,
            "block_number": self.block_number,
            "data": self.data,
            "from_address": self.from_address,
            "keys": self.keys,
            'event_index': self.event_index
        }