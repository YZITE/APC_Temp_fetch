import requests
from .base import ApcKind

class Cs141(ApcKind):
    def fetch(self, user, password):
        s = requests.Session()
        r = self.urlway(0, 'http://' + host + '/api/login', lambda xurl: s.post(xurl, data = {
            'userName': user,
            'password': password,
            'anonymous': '',
            'newPassword': '',
        }))

        try:
            r = self.urlway(1, 'http://' + host + '/api/devices/ups/report', lambda xurl: s.get(xurl))
        finally:
            self.urlway(2, 'http://' + host + '/api/logout', lambda xurl: s.post(xurl, data = { 'userName': user }))

        upsst = r.json()['ups']['valtable']
        self.eprint(F'{host}: [result]:', repr(upsst))
        return upsst

    @staticmethod
    def extract(upsst): return upsst['TEMPDEG']
