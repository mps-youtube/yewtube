def get_version_number():
    f = open("VERSION")
    version = None
    for i in f.readlines():
        if 'version' in i:
            version = i.split()[-1].strip()
    return version
__version__ = get_version_number()
__notes__ = "released on 28 Jan 2022"
__author__ = "iamtalhaasghar"
__license__ = "GPLv3"
__url__ = "https://github.com/iamtalhaasghar/yewtube"

from . import init
init.init()
from . import main
