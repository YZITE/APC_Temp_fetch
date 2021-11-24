class ApcKind:
    def __init__(self, verbose: bool, host: str, **kwargs):
        # forwards all unused arguments
        super().__init__(**kwargs)

        self._verbose = verbose
        self._host = host

    def eprint(self, *args, **kwargs):
        if self._verbose:
            print(*args, file=sys.stderr, **kwargs)

    def urlway(self, num: int, in_url, handler):
        self.eprint(F'{self._host}: [{num}]', in_url, end=' -> ')
        try:
            r = handler(in_url)
            self.eprint(r.url)
            return r
        except Exception as e:
            # we want to terminate the line cleanly
            self.eprint('ERROR:', e)
            raise

    def fetch(self, user: str, password: str):
        raise NotImplementedError

    @staticmethod
    def extract(upsst):
        """extract the temperature from the return value of the `fetch` method"""
        raise NotImplementedError
