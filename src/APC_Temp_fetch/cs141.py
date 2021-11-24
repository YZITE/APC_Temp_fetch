import requests
from .base import ApcKind

class Cs141(ApcKind):
    def fetch(self, user: str, password: str):
        base_url = F'http://{self._host}/api'
        upsst = None

        with requests.Session() as s:
            r = self.urlway(0, False, base_url + '/login', lambda xurl: s.post(xurl, data = {
                'userName': user,
                'password': password,
                'anonymous': '',
                'newPassword': '',
            }))

            try:
                r = self.urlway(1, False, base_url + '/devices/ups/report', s.get)
            finally:
                self.urlway(2, False, base_url + '/logout', lambda xurl: s.post(xurl, data = { 'userName': user }))

            upsst = r.json()['ups']['valtable']
            del r

        self.eprint(F'{self._host}: [result]:', repr(upsst))
        return upsst

    @staticmethod
    def extract(upsst) -> str: return upsst['TEMPDEG']
