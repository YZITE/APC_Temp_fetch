import requests
from . import OutputConfig

def extract_all(verbose, host, user, password):
    o = OutputConfig(verbose, host)
    s = requests.Session()
    r = o.urlway(0, 'http://' + host + '/api/login', lambda xurl: s.post(xurl, data = {
        'userName': user,
        'password': password,
        'anonymous': '',
        'newPassword': '',
    }))

    try:
        r = o.urlway(1, 'http://' + host + '/api/devices/ups/report', lambda xurl: s.get(xurl))
    finally:
        o.urlway(2, 'http://' + host + '/api/logout', lambda xurl: s.post(xurl, data = { 'userName': user }))

    upsst = r.json()['ups']['valtable']
    o.eprint(F'{host}: [result]:', repr(upsst))
    return upsst

def extract(verbose, host, user, password):
    return extract_all(verbose, host, user, password)['TEMPDEG']
