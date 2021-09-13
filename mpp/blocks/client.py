from mpp.blocks import BlockWithStatements, BlockWithSubBlocks
from mpp.constants import HTTP_CLIENT_STATEMENTS, HTTP_GET_CLIENT_BLOCKS, HTTP_POST_CLIENT_BLOCKS


class GetClient(BlockWithSubBlocks):
    VALID_STATEMENTS = HTTP_CLIENT_STATEMENTS
    VALID_BLOCKS = HTTP_GET_CLIENT_BLOCKS


class PostClient(BlockWithSubBlocks):
    VALID_STATEMENTS = HTTP_CLIENT_STATEMENTS
    VALID_BLOCKS = HTTP_POST_CLIENT_BLOCKS


class StagerClient(BlockWithStatements):
    VALID_STATEMENTS = HTTP_CLIENT_STATEMENTS

