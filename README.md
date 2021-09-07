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

## Help :construction_worker:

#### Join us in discussions
I use GitHub Discussions to talk about all sorts of topics related to this repo.

#### Open an issue
First, check out the [existing issues](https://github.com/brett-fitz/pyMalleableProfileParser/issues). If you spot 
something new, open an issue. We'll use the issue to have a conversation about the problem you want to fix, and I'll 
try to get to it as soon as I can.