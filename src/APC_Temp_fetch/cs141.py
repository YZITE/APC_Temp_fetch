import requests
from .base import ATF_LOGGER, ApcKind, NullAuth

class Cs141(ApcKind):
    def fetch(self, user: str, password: str):
        base_url = F'http://{self._host}/api'
        upsst = None

        with requests.Session() as s:
            s.auth = NullAuth()
            r = self.urlway(0, base_url + '/login', s.post, data = {
                'userName': user,
                'password': password,
                'anonymous': '',
                'newPassword': '',
            })

            try:
                r = self.urlway(1, base_url + '/devices/ups/report', s.get)
            finally:
                self.urlway(2, base_url + '/logout', s.post, data = { 'userName': user })

            upsst = r.json()['ups']['valtable']
            del r

        ATF_LOGGER.debug(F'{self._host}: [result] {repr(upsst)}')
        return upsst

    @staticmethod
    def extract(upsst) -> str: return upsst['TEMPDEG']
