import sys

class ApcKind:
    def __init__(self, verbose: bool, host: str, **kwargs):
        # forwards all unused arguments, to make this class usable as a mixin
        super().__init__(**kwargs) # type: ignore[call-arg]

        self._verbose = verbose
        self._host = host

    def eprint(self, *args, **kwargs) -> None:
        if self._verbose:
            print(*args, file=sys.stderr, **kwargs)

    def urlway(self, num: int, fix_encoding: bool, in_url, handler):
        self.eprint(F'{self._host}: [{num}]', in_url, end=' -> ')
        try:
            r = handler(in_url)
            self.eprint(r.url)
            if fix_encoding and (r.encoding is None):
                r.encoding = 'utf-8'
            return r
        except Exception as e:
            # we want to terminate the line cleanly
            self.eprint('ERROR:', e)
            raise

    def fetch(self, user: str, password: str):
        raise NotImplementedError

    @staticmethod
    def extract(upsst) -> str:
        """extract the temperature from the return value of the `fetch` method"""
        raise NotImplementedError
