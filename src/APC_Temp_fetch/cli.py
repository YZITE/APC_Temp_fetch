# output format: host[\t]temperature_in_°C
# NOTE: this program does not submit results to mqtt (separation of responsibilities)

import argparse
import signal
import time
from . import KINDS

# { source: https://code-maven.com/python-timeout
class TimeOutException(Exception):
    pass
def alarm_handler(signum, frame):
    raise TimeOutException('timeout reached')
# }

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class UnknownFetcher(Exception):
    pass
def run_one_handle_kind(verbose: bool, kind: str, host: str, user: str, password: str):
    x = None
    try:
        x = KINDS[kind]
    except KeyError:
        raise UnknownFetcher('unknown fetcher: ' + kind)
    val = x.extract(x(verbose, host).fetch(user, password))
    if val:
        print(f"{host}\t{val}")

def main_one():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("kind", help="APC interface kind (one of: old frmnc cs141)")
    parser.add_argument("host", help="connect to the host (APC) via HTTP")
    parser.add_argument("user", help="with the given user")
    parser.add_argument("password", help="with the given pass")
    parser.add_argument("--timeout", help="set a timeout (in seconds) for the whole execution (per host)", type=int)
    args = parser.parse_args()
    del parser
    signal.signal(signal.SIGALRM, alarm_handler)

    try:
        if args.timeout:
            signal.alarm(args.timeout)
        run_one_handle_kind(args.verbose, args.kind, args.host, args.user, args.password)
    except Exception as e:
        eprint(F"{args.host}: ERROR: {e}")
    signal.alarm(0)

def main_list():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("apclist", help="file containing list of 'kind host user password [timeout]'")
    args = parser.parse_args()
    del parser
    signal.signal(signal.SIGALRM, alarm_handler)
    verbose = args.verbose

    with open(args.apclist, 'r') as apclist:
        for line in apclist:
            parts = line.split()
            if not parts or parts[0] == '#':
                pass
            elif len(parts) < 4:
                eprint("ERROR: got invalid apclist line:", line)
            else:
                kind, host, user, password = parts[:4]
                try:
                    if len(parts) > 4:
                        signal.alarm(int(parts[4]))
                    run_one_handle_kind(verbose, kind, host, user, password)
                except Exception as e:
                    eprint(F'{host}: ERROR: {e}')
                signal.alarm(0)
