from starknetetl.mappers.block_mapper import BlockMapper
from starknetetl.mappers.transaction_mapper import TransactionMapper
from starknetetl.service.service import StarknetService
from blockchainetl_common.executors.batch_work_executor import BatchWorkExecutor
from blockchainetl_common.jobs.base_job import BaseJob
from blockchainetl_common.utils import validate_range


class ExportBlocksJob(BaseJob):
    def __init__(
            self,
            start_block,
            end_block,
            rpc,
            max_workers,
            item_exporter,
            batch_size,
            export_blocks=True,
            export_transactions=True
    ):
        validate_range(start_block, end_block)
        self.start_block = start_block
        self.end_block = end_block

        self.batch_work_executor = BatchWorkExecutor(batch_size, max_workers)
        self.item_exporter = item_exporter

        self.export_blocks = export_blocks
        self.export_transactions = export_transactions
        if not self.export_blocks and not self.export_transactions:
            raise ValueError('Need export_blocks or export_transactions')

        self.service = StarknetService(rpc)
        self.block_mapper = BlockMapper
        self.transaction_mapper = TransactionMapper

    def _start(self):
        self.item_exporter.open()

    def _export(self):
        self.batch_work_executor.execute(
            range(self.start_block, self.end_block + 1),
            self._export_batch,
            total_items=self.end_block - self.start_block + 1
        )

    def _export_batch(self, block_number_batch):
        blocks = self.service.get_blocks(block_number_batch)
        for block in blocks:
            self._export_block(block)
            self._export_transactions(block)

    def _export_block(self, block):
        if self.export_blocks:
            block = self.block_mapper.from_dict(block)
            self.item_exporter.export_item(block.to_dict())

    def _export_transactions(self, block):
        if self.export_transactions:
            txs = block.get('transactions')
            for index in range(len(txs)):
                self._export_transaction(txs[index], block, index)

    def _export_transaction(self, transaction, block, index):
        transaction = self.transaction_mapper.from_dict(transaction, block, index)
        self.item_exporter.export_item(transaction.to_dict())

    def _end(self):
        self.batch_work_executor.shutdown()
        self.item_exporter.close()
