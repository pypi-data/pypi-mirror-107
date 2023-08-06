from . import data
from . import chart
from . import mlearn
from . import model
from . import statmodel

from . import __eval

from pkg_resources import get_distribution as __dist

def version () :
    return __dist('anoapycore').version
