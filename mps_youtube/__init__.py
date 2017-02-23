__version__ = "0.2.7.1"
__notes__ = "released 6 July 2016"
__author__ = "np1"
__license__ = "GPLv3"
__url__ = "https://github.com/mps-youtube/mps-youtube"

from . import c, config
from .plugin import Plugin
from .util import dbg

from . import init
init.init()
from . import main
