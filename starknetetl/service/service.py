class StarknetService:
    def __init__(self, rpc):
        self.rpc = rpc

    @staticmethod
    def _check_error(res):
        assert 'error' not in res.keys(), res['error']

    def get_block(self, block_number):
        res = self.rpc.get_block(block_number)
        self._check_error(res)
        return res['result']

    def get_blocks(self, block_numbers):
        return [self.get_block(i) for i in block_numbers]

    def get_genesis_block(self):
        res = self.get_block(0)
        return res

    def get_block_timestamp(self, block_number):
        return block_number, int(self.get_block(block_number)['timestamp'])

    def get_genesis_block_timestamp(self):
        return self.get_block_timestamp(0)

    def get_latest_block_timestamp(self):
        res = self.rpc.get_latest_block()
        self._check_error(res)
        number = res['result']
        return self.get_block_timestamp(number)

    def get_transaction_receipt(self, transaction_hash):
        res = self.rpc.get_transaction_receipt(transaction_hash)
        try:
            self._check_error(res)
        except Exception as e:
            if res.get('error', {}).get('code') != -32603 and 'error' not in res.keys():
                raise Exception(res['error'])
            else:
                return {
                    "transaction_hash": transaction_hash,
                    "status": 'ERROR'
                }
        return res['result']

    def get_transaction_receipts(self, transaction_hashes):
        return [self.get_transaction_receipt(transaction_hash) for transaction_hash in transaction_hashes]

