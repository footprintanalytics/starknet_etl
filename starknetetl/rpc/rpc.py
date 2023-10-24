from base.rpc.rpc import BaseRpc


class StarknetRpc(BaseRpc):

    def get_block(self, number):
        return self.call('', data={
            "jsonrpc": "2.0",
            "method": "starknet_getBlockWithTxs",
            "params": [{"block_number": number}],
            "id": number
        })

    def get_transaction_receipt(self, tx_hash):
        return self.call('', data={
            "jsonrpc": "2.0",
            "method": "starknet_getTransactionReceipt",
            "params": [tx_hash],
            "id": tx_hash
        })

    def get_latest_block(self):
        return self.call('', data={
            "jsonrpc": "2.0",
            "method": "starknet_blockNumber",
            "params": [],
            "id": 'latest'
        })

    # 更多业务

