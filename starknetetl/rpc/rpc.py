import decimal
import json
from web3._utils.request import make_post_request


class StarknetRpc():
    def __init__(self, provider_uri, timeout=60):
        self.provider_uri = provider_uri
        self.timeout = timeout

    def call(self, endpoint, data, need_decode=True):
        text = json.dumps(data)
        request_data = text.encode('utf-8')
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }
        response = make_post_request(
            self.provider_uri + endpoint,
            request_data,
            timeout=self.timeout,
            headers=headers
        )
        if need_decode:
            response = self._decode_rpc_response(response)
        return response

    def _decode_rpc_response(self, response):
        response_text = response.decode('utf-8', errors='ignore')
        return json.loads(response_text, parse_float=decimal.Decimal)

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
