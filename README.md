# pyMalleableProfileParser
Parses Cobalt Strike malleable C2 profiles.

[![Latest version released on PyPi](https://img.shields.io/pypi/v/pymalleableprofileparser?style=flat-square)](https://pypi.org/project/pyMalleableProfileParser/)
[![License](https://img.shields.io/github/license/brett-fitz/pyMalleableProfileParser?style=flat-square)](https://github.com/brett-fitz/pyMalleableProfileParser/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/brett-fitz/pyMalleableProfileParser?style=flat-square)](https://github.com/brett-fitz/pyMalleableProfileParser/issues)

![Cobalt Strike Logo](https://raw.githubusercontent.com/brett-fitz/pyMalleableProfileParser/main/cobalt-strike-logo.png)


## Installation :gear:
```shell
pip3 install pyMalleableProfileParser
```

### Upgrading to the latest version
```shell
pip3 install --upgrade pyMalleableProfileParser
```


## Usage

### MalleableProfile class
```python
from mpp import MalleableProfile
mp = MalleableProfile(profile='/path/to/profile')
mp.profile
```

### Get attributes easily

### Options
Here is an example of getting the global option `jitter`:
```python
>> mp.jitter        
Option(option="jitter", value="0")
>> mp.jitter.option
'jitter'
>> mp.jitter.value
'0'
```
You can also access options in any block:
```python
>> mp.http_get.uri
Option(option="uri", value="/s/ref=nb_sb_noss_1/167-3294888-0262949/field-keywords=books")
```

### Statements
You can get statements in any block or sub-block:
```python
>> mp.http_get.client.Host
Statement(statement=header, key="Host", value="www.amazon.com")
```
```python
>> mp = MalleableProfile('bing_maps.profile')
>> mp.stage.transform_x86.ReflectiveLoader
Statement(statement=strrep, string="ReflectiveLoader", replace="")
```

### Blocks
Like statements, you can access any block or sub-block:
```python
>> mp.http_get
Block(name=http-get, data=[Option(option="uri", value="/s/ref=nb_sb_noss_1/167-3294888-0262949/field-keywords=books"), 
Block(name=client, data=[Statement(statement=header, key="Accept", value="*/*"), Statement(statement=header, key="Host", 
value="www.amazon.com"), Block(name=metadata, data=[Statement(statement=base64, value=""), Statement(statement=prepend, 
value="session-token="), Statement(statement=prepend, value="skin=noskin;"), Statement(statement=append, 
value="csm-hit=s-24KU11BB82RZSYGJ3BDK|1419899012996"), Statement(statement=header, key="Cookie", value="")])]), 
Block(name=server, data=[Statement(statement=header, key="Server", value="Server"), Statement(statement=header, 
key="x-amz-id-1", value="THKUYEZKCKPGY5T42PZT"), Statement(statement=header, key="x-amz-id-2", 
value="a21yZ2xrNDNtdGRsa212bGV3YW85amZuZW9ydG5rZmRuZ2tmZGl4aHRvNDVpbgo="), Statement(statement=header, 
key="X-Frame-Options", value="SAMEORIGIN"), Statement(statement=header, key="Content-Encoding", value="gzip"), Block(
name=output, data=[Statement(statement=print, value="")])])])
>> mp.http_get.server.output
Block(name=output, data=[Statement(statement=print, value="")])
```


## Validate a Profile
By default, `validate()` will validate Malleable Profiles for 4.0+. You can also specify a specific version. Note: a
warning will be displayed when setting dns options globally but will fail the validation if you specify version `4.3`.

**Example**
```python
>>> from mpp.profile import MalleableProfile
>>> mp = MalleableProfile('bing_maps.profile')
>>> mp.validate()
starting with v4.3, dns options have been moved into 'dns-beacon' block: dns_idle
starting with v4.3, dns options have been moved into 'dns-beacon' block: maxdns
starting with v4.3, dns options have been moved into 'dns-beacon' block: dns_sleep
starting with v4.3, dns options have been moved into 'dns-beacon' block: dns_stager_prepend
starting with v4.3, dns options have been moved into 'dns-beacon' block: dns_stager_subhost
starting with v4.3, dns options have been moved into 'dns-beacon' block: dns_max_txt
starting with v4.3, dns options have been moved into 'dns-beacon' block: dns_ttl
True
>>> mp.validate(version=4.3)
[(Option(option="dns_idle", value="8.8.8.8"), 'INVALID_OPTION'), (Option(option="maxdns", value="245"), 'INVALID_OPTION'), (Option(option="dns_sleep", value="0"), 'INVALID_OPTION'), (Option(option="dns_stager_prepend", value=""), 'INVALID_OPTION'), (Option(option="dns_stager_subhost", value=""), 'INVALID_OPTION'), (Option(option="dns_max_txt", value="252"), 'INVALID_OPTION'), (Option(option="dns_ttl", value="1"), 'INVALID_OPTION')]
>>> 

```


## Profile Structure (Dict)

**Example: amazon.profile**
```python
{'sleeptime': Option(option="sleeptime", value="5000"),
 'jitter': Option(option="jitter", value="0"),
 'maxdns': Option(option="maxdns", value="255"),
 'useragent': Option(option="useragent", value="Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"),
 'http-get': Block(name=http-get, data=[Option(option="uri", value="/s/ref=nb_sb_noss_1/167-3294888-0262949/field-keywords=books"), 
                                        Block(name=client, data=[Statement(statement=header, key="Accept", value="*/*"), 
                                                                 Statement(statement=header, key="Host", value="www.amazon.com"), 
                                                                 Block(name=metadata, data=[Statement(statement=base64, value=""), 
                                                                                            Statement(statement=prepend, value="session-token="), 
                                                                                            Statement(statement=prepend, value="skin=noskin;"), 
                                                                                            Statement(statement=append, value="csm-hit=s-24KU11BB82RZSYGJ3BDK|1419899012996"), 
                                                                                            Statement(statement=header, key="Cookie", value="")])]), 
                                        Block(name=server, data=[Statement(statement=header, key="Server", value="Server"), 
                                                                 Statement(statement=header, key="x-amz-id-1", value="THKUYEZKCKPGY5T42PZT"), 
                                                                 Statement(statement=header, key="x-amz-id-2", value="a21yZ2xrNDNtdGRsa212bGV3YW85amZuZW9ydG5rZmRuZ2tmZGl4aHRvNDVpbgo="), 
                                                                 Statement(statement=header, key="X-Frame-Options", value="SAMEORIGIN"), 
                                                                 Statement(statement=header, key="Content-Encoding", value="gzip"), 
                                                                 Block(name=output, data=[Statement(statement=print, value="")])])]),
 'http-post': Block(name=http-post, data=[Option(option="uri", value="/N4215/adj/amzn.us.sr.aps"), 
                                          Block(name=client, data=[Statement(statement=header, key="Accept", value="*/*"), 
                                                                   Statement(statement=header, key="Content-Type", value="text/xml"), 
                                                                   Statement(statement=header, key="X-Requested-With", value="XMLHttpRequest"), 
                                                                   Statement(statement=header, key="Host", value="www.amazon.com"), 
                                                                   Statement(statement=parameter, key="sz", value="160x600"), 
                                                                   Statement(statement=parameter, key="oe", value="oe=ISO-8859-1;"), 
                                                                   Block(name=id, data=[Statement(statement=parameter, key="sn", value="")]), 
                                                                   Statement(statement=parameter, key="s", value="3717"), 
                                                                   Statement(statement=parameter, key="dc_ref", value="http%3A%2F%2Fwww.amazon.com"), 
                                                                   Block(name=output, data=[Statement(statement=base64, value=""), 
                                                                                            Statement(statement=print, value="")])]), 
                                          Block(name=server, data=[Statement(statement=header, key="Server", value="Server"), 
                                                                   Statement(statement=header, key="x-amz-id-1", value="THK9YEZJCKPGY5T42OZT"), 
                                                                   Statement(statement=header, key="x-amz-id-2", value="a21JZ1xrNDNtdGRsa219bGV3YW85amZuZW9zdG5rZmRuZ2tmZGl4aHRvNDVpbgo="), 
                                                                   Statement(statement=header, key="X-Frame-Options", value="SAMEORIGIN"), 
                                                                   Statement(statement=header, key="x-ua-compatible", value="IE=edge"), 
                                                                   Block(name=output, data=[Statement(statement=print, value="")])])])}
```

## Help :construction_worker:

#### Join us in discussions
I use GitHub Discussions to talk about all sorts of topics related to this repo.

#### Open an issue
First, check out the [existing issues](https://github.com/brett-fitz/pyMalleableProfileParser/issues). If you spot 
something new, open an issue. We'll use the issue to have a conversation about the problem you want to fix, and I'll 
try to get to it as soon as I can.