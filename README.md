# pyMalleableProfileParser
Parses Cobalt Strike malleable C2 profiles.

![Cobalt Strike Logo](./cobalt-strike-logo.png)

## Installation :gear:
```shell
pip3 install pymalleableprofileparser
```

## Usage

### MalleableProfile class
```python
from mpp import MalleableProfile
mp = MalleableProfile(profile='/path/to/profile')
mp.profile      # profile as a dictionary
```

### Get attributes easily
```python
mp.sleeptime        # option
mp.http_get         # group
```

### Profile attribute structure (dict)
```python
profile = {
    'option': '',
    'group_name': {
        'option': '',
        'statements': ['statement'],
        'sub_group_name': {
            'option': '',
            'statements': ['statement'],
        }
    }
}
```
**Example: amazon.profile**
```python
{'sleeptime': '5000',
 'jitter': '0',
 'maxdns': '255',
 'useragent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
 'http-get': {'statements': [],
  'uri': '/s/ref=nb_sb_noss_1/167-3294888-0262949/field-keywords=books',
  'client': {'statements': ['header "Accept" "*/*";',
    'header "Host" "www.amazon.com";'],
   'metadata': {'statements': ['base64;',
     'prepend "session-token=";',
     'prepend "skin=noskin;";',
     'append "csm-hit=s-24KU11BB82RZSYGJ3BDK|1419899012996";',
     'header "Cookie";']}},
  'server': {'statements': ['header "Server" "Server";',
    'header "x-amz-id-1" "THKUYEZKCKPGY5T42PZT";',
    'header "x-amz-id-2" "a21yZ2xrNDNtdGRsa212bGV3YW85amZuZW9ydG5rZmRuZ2tmZGl4aHRvNDVpbgo=";',
    'header "X-Frame-Options" "SAMEORIGIN";',
    'header "Content-Encoding" "gzip";'],
   'output': {'statements': ['print;']}}},
 'http-post': {'statements': [],
  'uri': '/N4215/adj/amzn.us.sr.aps',
  'client': {'statements': ['header "Accept" "*/*";',
    'header "Content-Type" "text/xml";',
    'header "X-Requested-With" "XMLHttpRequest";',
    'header "Host" "www.amazon.com";',
    'parameter "sz" "160x600";',
    'parameter "oe" "oe=ISO-8859-1;";',
    'parameter "s" "3717";',
    'parameter "dc_ref" "http%3A%2F%2Fwww.amazon.com";'],
   'id': {'statements': ['parameter "sn";']},
   'output': {'statements': ['base64;', 'print;']}},
  'server': {'statements': ['header "Server" "Server";',
    'header "x-amz-id-1" "THK9YEZJCKPGY5T42OZT";',
    'header "x-amz-id-2" "a21JZ1xrNDNtdGRsa219bGV3YW85amZuZW9zdG5rZmRuZ2tmZGl4aHRvNDVpbgo=";',
    'header "X-Frame-Options" "SAMEORIGIN";',
    'header "x-ua-compatible" "IE=edge";'],
   'output': {'statements': ['print;']}}}}
```

## Help :construction_worker:

#### Join us in discussions
I use GitHub Discussions to talk about all sorts of topics related to this repo.

#### Open an issue
First, check out the [existing issues](https://github.com/brett-fitz/pyMalleableProfileParser/issues). If you spot 
something new, open an issue. We'll use the issue to have a conversation about the problem you want to fix, and I'll 
try to get to it as soon as I can.