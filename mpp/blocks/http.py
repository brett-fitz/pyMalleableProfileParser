from mpp.blocks import BlockWithSubBlocks, BlockWithStatements
from mpp.constants import HTTP_OPTIONS, HTTP_BLOCKS, HTTP_CONFIG_OPTIONS, HTTP_CONFIG_STATEMENTS, HTTP_STAGER_OPTIONS


class HTTPConfig(BlockWithStatements):
    VALID_OPTIONS = HTTP_CONFIG_OPTIONS
    VALID_STATEMENTS = HTTP_CONFIG_STATEMENTS


class BaseHTTP(BlockWithSubBlocks):
    VALID_OPTIONS = HTTP_OPTIONS
    VALID_BLOCKS = HTTP_BLOCKS


class HTTPGet(BaseHTTP):
    pass


class HTTPPost(BaseHTTP):
    pass


class HTTPStager(BaseHTTP):
    VALID_OPTIONS = HTTP_STAGER_OPTIONS
