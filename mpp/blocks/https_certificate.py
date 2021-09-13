from mpp.blocks import BlockWithOptions
from mpp.constants import HTTPS_CERTIFICATE_OPTIONS


class HTTPSCertificate(BlockWithOptions):
    VALID_OPTIONS = HTTPS_CERTIFICATE_OPTIONS
