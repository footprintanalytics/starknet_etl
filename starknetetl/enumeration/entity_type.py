class EntityType:
    BLOCK = 'block'
    TRANSACTION = 'transaction'
    RECEIPT = 'receipt'
    LOG = 'log'
    EVENT = 'event'
    MESSAGE = 'message'
    TOKEN_TRANSFER = 'token_transfer'
    TRACE = 'trace'
    CONTRACT = 'contract'
    TOKEN = 'token'

    ALL_FOR_STREAMING = [BLOCK, TRANSACTION, EVENT, MESSAGE, TOKEN_TRANSFER]
    ALL_FOR_INFURA = [BLOCK, TRANSACTION, EVENT, MESSAGE, TOKEN_TRANSFER]
