from .main import init
from .main import __version__, __notes__, __author__, __license__, __url__
from .config import Config
from . import c
from .plugin import Plugin, registerPlugin
from .util import dbg

init()
