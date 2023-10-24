class ReceiptMapper:
    def __init__(self, block_number, block_hash, actual_fee, event_count, messages_sent_count,
                 status, transaction_hash, type, contract_address):
        self.block_number = block_number
        self.block_hash = block_hash
        self.actual_fee = actual_fee
        self.event_count = event_count
        self.messages_sent_count = messages_sent_count
        self.status = status
        self.transaction_hash = transaction_hash
        self.type = type
        self.contract_address = contract_address

    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get("block_number"),
            data.get("block_hash"),
            int(str(data.get("actual_fee")), 16) if data.get("actual_fee") is not None else None,
            len(data.get("events", [])),
            len(data.get("messages_sent", [])),
            data["finality_status"],
            data["transaction_hash"],
            data.get("type"),
            data.get("contract_address")
        )

    def to_dict(self):
        return {
            "type": 'receipt',
            "block_number": self.block_number,
            "block_hash": self.block_hash,
            "actual_fee": self.actual_fee,
            "event_count": self.event_count,
            "messages_sent_count": self.messages_sent_count,
            "status": self.status,
            "transaction_hash": self.transaction_hash,
            "_type": self.type,
            "contract_address": self.contract_address
        }