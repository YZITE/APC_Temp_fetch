import requests
from . import eprint

def extract(verbose, host, user, password):
    xurl = 'http://' + host + '/api/login'
    eprint('[0]', xurl, end=' -> ', verbose=verbose)
    s = requests.Session()
    r = s.post(xurl, data = {
        'userName': user,
        'password': password,
        'anonymous': '',
        'newPassword': '',
    })
    eprint(r.url, verbose=verbose)

    xurl = 'http://' + host + '/api/devices/ups/report'
    eprint('[1]', xurl, verbose=verbose)

    try:
        r = s.get(xurl)
        upsst = r.json()['ups']['valtable']
    finally:
        xurl = 'http://' + host + '/api/logout'
        eprint('[2]', xurl, verbose=verbose)
        r = s.post(xurl, data = { 'userName': user })

    eprint('[result]: ' + repr(upsst), verbose=verbose)
    return upsst['TEMPDEG']
