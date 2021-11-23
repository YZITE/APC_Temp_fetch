def eprint(*args, **kwargs):
    if 'verbose' in kwargs:
        if not kwargs['verbose']:
            return
        del kwargs['verbose']
    print(*args, file=sys.stderr, **kwargs)

def my_urlway(verbose, host, num, in_url, handler):
    if verbose:
        print(F'{host}: [{num}]', in_url, end=' -> ', file=sys.stderr)
    try:
        r = handler(in_url)
        if verbose:
            print(r.url)
        return r
    except Exception as e:
        if verbose:
            # we want to terminate the line cleanly
            print('ERROR:', e)
        raise
