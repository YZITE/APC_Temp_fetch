import requests
from urllib.parse import urljoin
from .base import ApcKind

class UpsParserStateMachine:
    def __init__(self) -> None:
        self.upsst = {}
        self.state = self.wait_for_upss
        self.key = ''

    def wait_for_upss(self, line: str) -> None:
        if "UPS Status" in line:
            self.state = self.handle_kov_start

    def handle_kov_start(self, line: str) -> None:
        if line == '<div class="dataName">':
            self.key = ''
            self.state = self.handle_key
        elif self.key and line == '<div class="dataValue">':
            self.state = self.handle_value

    def handle_key(self, line: str) -> None:
        if "</span>" in line:
            self.key = line.split('<', 2)[0]
        elif line == '</div>':
            self.key = ''
        else:
            return
        self.state = self.handle_kov_start

    def handle_value(self, line: str) -> None:
        if line == '</div>':
            self.key = ''
            self.state = self.handle_kov_start
        elif '<span ' not in line:
            tmp = line.split('<', 2)[0].replace('&nbsp;', '').lstrip()
            if self.key not in self.upsst:
                self.upsst[self.key] = tmp
            else:
                self.upsst[self.key] += ' ' + tmp

class Frmnc(ApcKind):
    def fetch(self, user, password):
        base_url = "http://" + self.host
        r = o.urlway(0, base_url, requests.get)
        forml = [value for value in r.text.splitlines() if "name=\"frmLogin\"" in value][0]
        next_url = urljoin(base_url,
            [value for value in forml.split() if "action=" in value][0].split('=', 2)[1].split('"', 3)[1])
        del forml

        r = o.urlway(1, next_url, lambda xurl: requests.post(next_url, data = {
            'login_username': args.user,
            'login_password': args.password,
        }))

        try:
            statemach = UpsParserStateMachine()
            for line in r.text.splitlines():
                (statemach.state)(line)
            upsst = statemach.upsst
            del statemach
        finally:
            o.urlway(2, urljoin(r.url, "logout.htm"), requests.get)

        o.eprint(F'{self.host}: [result]:', repr(upsst))
        return upssst

    @staticmethod
    def extract(upsst): return upsst['Internal Temperature'].replace('&deg;C', '')
