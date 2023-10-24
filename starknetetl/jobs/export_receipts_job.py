
from starknetetl.mappers.event_mapper import EventMapper
from starknetetl.mappers.receipt_mapper import ReceiptMapper
from starknetetl.mappers.message_mapper import MessageMapper
from starknetetl.mappers.token_transfer_mapper import TokenTransferMapper
from starknetetl.service.service import StarknetService
from blockchainetl_common.executors.batch_work_executor import BatchWorkExecutor
from blockchainetl_common.jobs.base_job import BaseJob

TOKEN_TRANSFER_EVENT = "0x99cd8bde557814842a3121e8ddfd433a539b8c9f14bf31ebf108d12e6196e9"

class ExportReceiptsJob(BaseJob):
    def __init__(
            self,
            transaction_hashes_iterable,
            batch_size,
            rpc,
            max_workers,
            item_exporter,
            export_receipts=True,
            export_messages=True,
            export_events=True,
            export_token_transfers=True):
        self.rpc = rpc
        self.transaction_hashes_iterable = transaction_hashes_iterable

        self.item_exporter = item_exporter
        self.batch_work_executor = BatchWorkExecutor(batch_size, max_workers)  # 这里因为sui有自带的batch功能, 这里默认size为1

        self.export_receipts = export_receipts
        self.export_events = export_events
        self.export_messages = export_messages
        self.export_token_transfers = export_token_transfers
        if not self.export_token_transfers and not self.export_events and not self.export_messages and not self.export_receipts:
            raise ValueError(
                'At least one of export_token_transfers or export_events or export_messages or export_receipts')

        self.service = StarknetService(rpc)
        self.token_transfer_mapper = TokenTransferMapper
        self.event_mapper = EventMapper
        self.message_mapper = MessageMapper
        self.receipt_mapper = ReceiptMapper

    def _start(self):
        self.item_exporter.open()

    def _export(self):
        self.batch_work_executor.execute(self.transaction_hashes_iterable, self._export_alls)

    def _export_alls(self, transaction_hashes):
        receipts = self.service.get_transaction_receipts(transaction_hashes)
        for receipt in receipts:
            self._export_receipts(receipt)
            self._export_events_and_token_transfers(receipt)
            self._export_messages(receipt)

    def _export_receipts(self, receipt_info):
        if self.export_receipts:
            receipt = self.receipt_mapper.from_dict(receipt_info)
            self.item_exporter.export_item(receipt.to_dict())

    def _export_events_and_token_transfers(self, receipt):
        if receipt.get('execution_status') != 'ERROR':
            receipts_info = {
                "transaction_hash": receipt.get("transaction_hash"),
                "block_hash": receipt.get("block_hash"),
                "block_number": receipt.get("block_number"),
                }
            events = receipt.get('events')
            for index in range(len(events)):
                self._export_event(index, events[index], receipts_info)
                self._export_token_transfer(index, events[index], receipts_info)


    def _export_event(self, event_index, event_info, receipt_info):
        if self.export_events:
            event = self.event_mapper.from_dict(event_info, receipt_info, event_index)
            self.item_exporter.export_item(event.to_dict())

    def _export_token_transfer(self, event_index, event_info, receipt_info):

        if self.export_token_transfers and event_info.get("keys") and (event_info.get("keys")[0] == TOKEN_TRANSFER_EVENT):
            key_len = len(event_info.get("keys"))
            if key_len == 1:
                token_transfers = self.token_transfer_mapper.from_dict(event_info, receipt_info, event_index)
                self.item_exporter.export_item(token_transfers.to_dict())
            elif key_len != 3:
                key_info = event_info.get("keys")
                token_transfer_info = {"data": [key_info[1], key_info[2], key_info[3]], "from_address": event_info["from_address"]}
                token_transfers = self.token_transfer_mapper.from_dict(token_transfer_info, receipt_info, event_index)
                self.item_exporter.export_item(token_transfers.to_dict())


    def _export_messages(self, receipt):
        if self.export_messages and receipt.get('execution_status') != 'ERROR' and len(receipt.get("messages_sent")) > 0:
            receipts_info = {
                "transaction_hash": receipt.get("transaction_hash"),
                "block_hash": receipt.get("block_hash"),
                "block_number": receipt.get("block_number"),
                "type": receipt.get("type")
            }
            for message_info in receipt.get("messages_sent"):
                message = self.message_mapper.from_dict(receipts_info, message_info)
                self.item_exporter.export_item(message.to_dict())

    def _end(self):
        self.batch_work_executor.shutdown()
        self.item_exporter.close()
