from mpp.blocks import TransformBlock
from mpp.constants import HTTP_SERVER_TERMINATION_STATEMENTS


class Output(TransformBlock):
    pass


class OutputServer(TransformBlock):
    VALID_TERMINATION_STATEMENTS = HTTP_SERVER_TERMINATION_STATEMENTS
