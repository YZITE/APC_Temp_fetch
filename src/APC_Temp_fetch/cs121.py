from html.parser import HTMLParser
import requests
from collections.abc import Iterable
from typing import Dict, Optional, Tuple
from .base import ATF_LOGGER, ApcKind

class UpsStatEntity:
    def __init__(self, ident: str) -> None:
       self.ident = ident
       self.description = ''
       self.value = ''

# e.g. """ <tr onMouseOver="TTshow('upsstat_11')" onMouseOut="TThide()"><td class="maina">Battery&nbsp;Temperature</td><td class="mainb" width="100%" colspan=3>30.0&nbsp;</td></tr>"""

class UpsParserStateMachine(HTMLParser):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.stats: Dict[str, Tuple[str, str]] = dict()
        self.__sel: Optional[UpsStatEntity] = None
        self.__selty = None

    def handle_starttag(self, tag: str, attrs) -> None:
        attrs = {i[0]: i[1] for i in attrs}
        if tag == 'tr':
            if ('onmouseover' in attrs) and (attrs.get('onmouseout') == 'TThide()'):
                self.__sel = UpsStatEntity(attrs['onmouseover'].replace("TTshow('upsstat_", '').replace("')", ''))
                self.__selty = None
        elif self.__sel and tag == 'td':
            self.__selty = attrs.get('class')

    @staticmethod
    def mangle_value(x: str) -> str:
        return x.strip().replace('\xa0', ' ').removeprefix('_dw("').removesuffix('")')

    def handle_endtag(self, tag: str) -> None:
        if not self.__sel:
            return

        if tag == 'td':
            self.__selty = None
        elif tag == 'tr' and self.__sel.description:
            self.stats[self.mangle_value(self.__sel.description)] = (self.__sel.ident, self.mangle_value(self.__sel.value))
            self.__selty = None
            self.__sel = None

    def handle_entityref(self, name: str) -> None:
        if name == '&nbsp;':
            self.handle_data(' ')

    def handle_data(self, data: str) -> None:
        if (not self.__sel) or (not self.__selty):
            return

        if self.__selty == 'maina':
            self.__sel.description += data
        elif self.__selty == 'mainb':
            self.__sel.value += data

class Cs121(ApcKind):
    @staticmethod
    def parse(rlns: Iterable[str]) -> Dict[str, Tuple[str, str]]:
        statemach = UpsParserStateMachine()
        for line in rlns:
            statemach.feed(line)
        statemach.close()
        return statemach.stats

    def fetch(self, user: str, password: str):
        # we ignore user and password
        rlns = self.urlway(0, F'http://{self._host}/main.shtml', requests.get, stream = True).iter_lines(decode_unicode=True)
        upsst = self.parse(rlns)
        ATF_LOGGER.debug(F'{self._host}: [result] {repr(upsst)}')
        return upsst

    @staticmethod
    def extract(upsst: Dict[str, Tuple[str, str]]) -> Optional[str]:
        for i in ['UPS Temperature', 'Battery Temperature']:
            j = upsst.get(i)
            if j: return j[1]
        return None
