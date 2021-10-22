from mpp.profile import MalleableProfile

path = __file__[:-7]

# Amazon
print('[*] running amazon test')
amazon = MalleableProfile(f'{path}amazon.profile')
if amazon.jitter.value == '0':
    print('[+] passed global option test')
else:
    print('[!] failed global option test')

if amazon.http_get.client.Host.value == 'www.amazon.com':
    print('[+] passed sub-block statement test')
else:
    print('[!] failed sub-block statement test')

if isinstance(amazon.validate(), bool):
    print('[+] passed validate test')
else:
    print('[!] failed validate test')


# Bing Maps
print('[*] running bing_maps test')
bing_maps = MalleableProfile(f'{path}bing_maps.profile')
if bing_maps.sleeptime.value == '38500':
    print('[+] passed global option test')
else:
    print('[!] failed global option test')

if bing_maps.http_get.client.metadata.base64.value == '':
    print('[+] passed sub-block statement test')
else:
    print('[!] failed sub-block statement test')

if isinstance(bing_maps.validate(), bool):
    print('[+] passed validate test')
else:
    print('[!] failed validate test')


# Mayo Clinic
print('[*] running mayoclinic test')
mayo_clinic = MalleableProfile(f'{path}mayoclinic.profile')
if mayo_clinic.useragent.value == 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko':
    print('[+] passed global option test')
else:
    print('[!] failed global option test')

if mayo_clinic.stage.transform_x86.ReflectiveLoader.replace == '':
    print('[+] passed sub-block statement test')
else:
    print('[!] failed sub-block statement test')

if isinstance(mayo_clinic.validate(), list):
    print('[+] passed validate test')
else:
    print('[!] failed validate test')
