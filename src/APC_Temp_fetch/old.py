import requests
from .base import ApcKind

class Old(ApcKind):
    def fetch(self, user: str, password: str):
        return self.urlway(0, True, 'http://' + self._host + '/upsstat.htm',
            lambda xurl: requests.get(xurl, auth = (user, password), stream=True)).iter_lines(decode_unicode=True)

    @staticmethod
    def extract(rlns) -> str:
        *_, last = filter(lambda line: "Internal Temperature" in line, rlns)
        return last
