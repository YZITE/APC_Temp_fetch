import requests
from .base import ApcKind

class Old(ApcKind):
    def fetch(self, user, password):
        return self.urlway(0, 'http://' + self.host + '/upsstat.htm',
            lambda xurl: requests.get(xurl, auth = (user, password))).text

    @staticmethod
    def extract(rtxt): return filter(lambda line: "Internal Temperature" in line, rtxt.splitlines())[-1]
