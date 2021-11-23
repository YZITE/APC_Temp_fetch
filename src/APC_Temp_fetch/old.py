import requests
from . import OutputConfig

def extract_all(verbose, host, user, password):
    r = OutputConfig(verbose, host).urlway(0, 'http://' + host + '/upsstat.htm',
        lambda xurl: requests.get(xurl, auth = (user, password)))
    return r.text

def extract(verbose, host, user, password):
    return filter(lambda line: "Internal Temperature" in line, extract_all(verbose, host, user, password).splitlines())[-1]
