class BlockMapper:
    def __init__(self, block_hash, parent_hash, block_number, new_root, block_timestamp, sequencer_address,
                 transactions, status):
        self.block_hash = block_hash
        self.parent_hash = parent_hash
        self.block_number = block_number
        self.new_root = new_root
        self.block_timestamp = block_timestamp
        self.sequencer_address = sequencer_address
        self.transaction_count = len(transactions)
        self.status = status

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["block_hash"],
            data["parent_hash"],
            data["block_number"],
            data["new_root"],
            data["timestamp"],
            data["sequencer_address"],
            data["transactions"],
            data["status"]
        )

    def to_dict(self):
        return {
            'type': "block",
            "block_hash": self.block_hash,
            "parent_hash": self.parent_hash,
            "block_number": self.block_number,
            "new_root": self.new_root,
            "block_timestamp": self.block_timestamp,
            "sequencer_address": self.sequencer_address,
            "transaction_count": self.transaction_count,
            "status": self.status
        }
