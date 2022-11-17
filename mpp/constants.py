from typing import Set, Dict

# Constants
DELIM: str = ';'
START_BLOCK_DELIM: str = '{'
END_BLOCK_DELIM: str = '}'

# Errors
INVALID_STATEMENT: str = 'INVALID_STATEMENT'
INVALID_TERMINATION_STATEMENT: str = 'INVALID_TERMINATION_STATEMENT'
INVALID_TRANSFORM_STATEMENT: str = 'INVALID_TRANSFORM_STATEMENT'
INVALID_OPTION: str = 'INVALID_OPTION'
INVALID_BLOCK: str = 'INVALID_BLOCK'
INVALID_VARIANT: str = 'INVALID_VARIANT'

# Special Strings
SPECIAL_STRINGS: Set[str] = {
    '\n',
    '\r',
    '\t',
    r'\u####',
    r'\x##',
    r'\\'
}

# All Statements
STATEMENTS: Set[str] = {
    'append',
    'base64',
    'base64url',
    'CreateRemoteThread',
    'CreateThread',
    'data',
    'header',
    'mask',
    'netbios',
    'netbiosu',
    'NtQueueApcThread',
    'NtQueueApcThread-s',
    'parameter',
    'prepend',
    'print',
    'RtlCreateUserThread',
    'SetThreadContext',
    'string',
    'stringw',
    'strrep',
    'uri-append'
}

# General Statements
# Data Transform
DATA_TRANSFORM_STATEMENTS: Set[str] = {
    'append',
    'base64',
    'base64url',
    'mask',
    'netbios',
    'netbiosu',
    'prepend'
}

# Termination
TERMINATION_STATEMENTS: Set[str] = {
    'header',
    'parameter',
    'print',
    'uri-append'
}
HTTP_SERVER_TERMINATION_STATEMENTS: Set[str] = {
    'print'
}

# Global Options
GLOBAL_OPTIONS: Set[str] = {
    'data_jitter',
    'headers_remove',
    'host_stage',
    'jitter',
    'pipename_stager',
    'pipename',
    'sample_name',
    'sleeptime',
    'smb_frame_header',
    'ssh_banner',
    'ssh_pipename',
    'tcp_frame_header',
    'tcp_port',
    'useragent'
}

# Blocks
# Profile Variants
PROFILE_VARIANTS: Set[str] = {
    'http-get',
    'http-post',
    'http-stager',
    'https-certificate',
    'dns-beacon'
}
PROFILE_BLOCKS: Set[str] = {
    'http-config',
    'http-get',
    'http-post',
    'http-stager',
    'https-certificate',
    'code-signer',
    'dns-beacon',
    'stage',
    'process-inject',
    'post-inject',
    'post-ex'
}
DATA_TRANSFORM_BLOCKS: Set[str] = {
    'metadata',
    'output',
    'id'
}

# http-config
HTTP_CONFIG_STATEMENTS: Set[str] = {
    'header'
}
HTTP_CONFIG_OPTIONS: Set[str] = {
    'trust_x_forwarded_for',
    'block_useragents',
    'allow_useragents'
}
# http-get, http-post, http-stager generics
HTTP_OPTIONS: Set[str] = {
    'uri',
    'verb'
}
HTTP_BLOCKS: Set[str] = {
    'client',
    'server'
}
HTTP_CLIENT_STATEMENTS: Set[str] = {
    'header',
    'parameter'
}
HTTP_SERVER_BLOCKS: Set[str] = {
    'output'
}

# http-get
# http-get.client
HTTP_GET_CLIENT_BLOCKS: Set[str] = {
    'metadata'
}

# http-post
# http-post.client
HTTP_POST_CLIENT_BLOCKS: Set[str] = {
    'id',
    'output'
}

# http-stager
HTTP_STAGER_OPTIONS: Set[str] = {
    'uri_x86',
    'uri_x64'
}

# https-certificate
HTTPS_CERTIFICATE_OPTIONS: Set[str] = {
    'CN',
    'C',
    'L',
    'OU',
    'O',
    'ST',
    'validity',
    'keystore',
    'password'
}

# dns-beacon
DNS_BEACON_OPTIONS: Set[str] = {
    'dns_idle',
    'dns_max_txt',
    'dns_sleep',
    'dns_stager_prepend',
    'dns_stager_subhost',
    'dns_ttl',
    'maxdns',
    'beacon',
    'get_AAAA',
    'get_A',
    'get_TXT',
    'put_metadata',
    'put_output',
    'ns_response'
}

# code-signer
CODE_SIGNER_OPTIONS: Set[str] = {
    'alias',
    'digest_algorithm',
    'keystore',
    'password',
    'timestamp',
    'timestamp_url'
}

# stage
STAGE_STATEMENTS: Set[str] = {
    'stringw',
    'string',
    'data'
}
STAGE_BLOCKS: Set[str] = {
    'transform-x86',
    'transform-x64'
}
STAGE_TRANSFORM_STATEMENTS: Set[str] = {
    'prepend',
    'append',
    'strrep'
}
STAGE_OPTIONS: Set[str] = {
    'allocator',
    'cleanup',
    'magic_mz_x86',
    'magic_mz_x64',
    'magic_pe',
    'module_x64',
    'module_x86',
    'obfuscate',
    'sleep_mask',
    'smartinject',
    'userwx',
    'stomppe',
    'checksum',
    'compile_time',
    'entry_point',
    'image_size_x64',
    'image_size_x86',
    'name',
    'rich_header'
}

# process-inject
PROCESS_INJECT_BLOCKS: Set[str] = {
    'transform-x86',
    'transform-x64',
    'execute'
}
PROCESS_INJECT_OPTIONS: Set[str] = {
    'allocator',
    'min_alloc',
    'startrwx',
    'userwx'
}
PROCESS_INJECT_TRANSFORM_STATEMENTS: Set[str] = {
    'prepend',
    'append'
}
PROCESS_INJECT_EXECUTE_STATEMENTS: Set[str] = {
    'CreateThread',
    'CreateRemoteThread',
    'NtQueueApcThread',
    'NtQueueApcThread-s',
    'RtlCreateUserThread',
    'SetThreadContext'
}

# post-ex
POST_EX_OPTIONS: Set[str] = {
    'spawnto_x86',
    'spawnto_x64',
    'obfuscate',
    'pipename',
    'smartinject',
    'thread_hint',
    'amsi_disable',
    'keylogger'
}

PROFILE: Dict = {
    'http-config': {
        'options': HTTP_CONFIG_OPTIONS,
        'statements': HTTP_CONFIG_STATEMENTS,
        'blocks': set()
    },
    'http-get': {
        'options': HTTP_OPTIONS,
        'statements': set(),
        'blocks': HTTP_BLOCKS
    },
    'http-get.client': {
        'options': set(),
        'statements': HTTP_CLIENT_STATEMENTS,
        'blocks': HTTP_GET_CLIENT_BLOCKS
    },
    'http-get.client.metadata': {
        'options': set(),
        'statements': DATA_TRANSFORM_STATEMENTS,
        'blocks': set()
    },
    'http-get.server': {
        'options': set(),
        'statements': HTTP_CLIENT_STATEMENTS,
        'blocks': HTTP_SERVER_BLOCKS
    },
    'http-get.server.output': {
        'options': set(),
        'statements': DATA_TRANSFORM_STATEMENTS,
        'blocks': set()
    },
    'http-post': {
        'options': HTTP_OPTIONS,
        'statements': set(),
        'blocks': HTTP_BLOCKS
    },
    'http-post.client': {
        'options': set(),
        'statements': HTTP_CLIENT_STATEMENTS,
        'blocks': HTTP_POST_CLIENT_BLOCKS
    },
    'http-post.client.id': {
        'options': set(),
        'statements': DATA_TRANSFORM_STATEMENTS,
        'blocks': set()
    },
    'http-post.client.output': {
        'options': set(),
        'statements': DATA_TRANSFORM_STATEMENTS,
        'blocks': set()
    },
    'http-post.server': {
        'options': set(),
        'statements': HTTP_CLIENT_STATEMENTS,
        'blocks': HTTP_SERVER_BLOCKS
    },
    'http-post.server.output': {
        'options': set(),
        'statements': DATA_TRANSFORM_STATEMENTS,
        'blocks': set()
    },
    'http-stager': {
        'options': HTTP_STAGER_OPTIONS,
        'statements': set(),
        'blocks': HTTP_BLOCKS
    },
    'http-stager.client': {
        'options': set(),
        'statements': HTTP_CLIENT_STATEMENTS,
        'blocks': set()
    },
    'http-stager.server': {
        'options': set(),
        'statements': HTTP_CLIENT_STATEMENTS,
        'blocks': HTTP_SERVER_BLOCKS
    },
    'http-stager.server.output': {
        'options': set(),
        'statements': DATA_TRANSFORM_STATEMENTS,
        'blocks': set()
    },
    'https-certificate': {
        'options': HTTPS_CERTIFICATE_OPTIONS,
        'statements': set(),
        'blocks': set()
    },
    'code-signer': {
        'options': CODE_SIGNER_OPTIONS,
        'statements': set(),
        'blocks': set()
    },
    'dns-beacon': {
        'options': DNS_BEACON_OPTIONS,
        'statements': set(),
        'blocks': set()
    },
    'stage': {
        'options': STAGE_OPTIONS,
        'statements': STAGE_STATEMENTS,
        'blocks': STAGE_BLOCKS
    },
    'stage.transform-x86': {
        'options': set(),
        'statements': STAGE_TRANSFORM_STATEMENTS,
        'blocks': set()
    },
    'stage.transform-x64': {
        'options': set(),
        'statements': STAGE_TRANSFORM_STATEMENTS,
        'blocks': set()
    },
    'process-inject': {
        'options': PROCESS_INJECT_OPTIONS,
        'statements': set(),
        'blocks': PROCESS_INJECT_BLOCKS
    },
    'process-inject.transform-x64': {
        'options': set(),
        'statements': DATA_TRANSFORM_STATEMENTS,
        'blocks': set()
    },
    'process-inject.transform-x86': {
        'options': set(),
        'statements': DATA_TRANSFORM_STATEMENTS,
        'blocks': set()
    },
    'process-inject.execute': {
        'options': set(),
        'statements': PROCESS_INJECT_EXECUTE_STATEMENTS,
        'blocks': set()
    },
    'post-ex': {
        'options': POST_EX_OPTIONS,
        'statements': set(),
        'blocks': set()
    }
}
