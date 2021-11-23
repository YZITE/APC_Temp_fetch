import requests
from . import eprint

def extract(verbose, host, user, password):
    xurl = 'http://' + host + '/upsstat.htm'
    eprint('[0]', xurl, verbose=verbose)
    r = requests.get('http://' + host + '/upsstat.htm', auth = (user, password))
    return filter(lambda line: "Internal Temperature" in line, r.text.splitlines())[-1]
