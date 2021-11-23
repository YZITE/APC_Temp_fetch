from .old import Old
from .frmnc import Frmnc
from .cs141 import Cs141

__all__ = ['KINDS']

KINDS = {
    'old': Old,
    'frmnc': Frmnc,
    'cs141': Cs141,
}
