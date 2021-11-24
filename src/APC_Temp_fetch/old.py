import requests
from .base import ApcKind

class Old(ApcKind):
    def fetch(self, user: str, password: str):
        return self.urlway(0, True, 'http://' + self._host + '/upsstat.htm',
            lambda xurl: requests.get(xurl, auth = (user, password), stream=True)).iter_lines(decode_unicode=True)

    @staticmethod
    def extract(rlns) -> str:
        sel = ''
        for line in rlns:
            if "Internal Temperature" in line:
                sel = next(rlns).split('>')[2].split('<')[0]
        return sel
