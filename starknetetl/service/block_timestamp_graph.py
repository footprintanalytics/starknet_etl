from blockchainetl_common.graph.graph_operations import Point
from starknetetl.service.service import StarknetService


class StarknetBlockTimestampGraph:
    def __init__(self, rpc):
        self._service = StarknetService(rpc)

    def get_first_point(self):
        res = self._service.get_genesis_block_timestamp()
        return self.block_to_point(*res)

    def get_last_point(self):
        res = self._service.get_latest_block_timestamp()
        return self.block_to_point(*res)

    def get_point(self, block_number):
        res= self._service.get_block_timestamp(block_number)
        return self.block_to_point(*res)

    def get_points(self, block_numbers):
        return [self.block_to_point(*self._service.get_block_timestamp(block)) for block in block_numbers]

    @staticmethod
    def block_to_point(number, timestamp):
        return Point(number, timestamp)
