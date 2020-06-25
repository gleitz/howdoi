import os
import sys


if sys.version < '3':
    import codecs
    # Handling Unicode: http://stackoverflow.com/a/6633040/305414
    def u(x):
        return codecs.unicode_escape_decode(x)[0]
else:
    def u(x):
        return x


# rudimentary standardized 3-level log output


def _print_err(x):
    print("[ERROR] " + x)


_print_ok = print  # noqa: E305


def _print_dbg(x):
    print("[DEBUG] " + x)  # noqa: E302


def _random_int(width):
    bres = os.urandom(width)
    if sys.version < '3':
        ires = int(bres.encode('hex'), 16)
    else:
        ires = int.from_bytes(bres, 'little')

    return ires


def _random_choice(seq):
    return seq[_random_int(1) % len(seq)]
