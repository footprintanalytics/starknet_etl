
from starknetetl.service.block_timestamp_graph import StarknetBlockTimestampGraph
from base.service.graph_operations import GraphOperations
from base.service.block_range_service import BlockRangeService


class StarknetBlockRangeService(BlockRangeService):
    def __init__(self, rpc):
        graph = StarknetBlockTimestampGraph(rpc)
        self._graph_operations = GraphOperations(graph)
