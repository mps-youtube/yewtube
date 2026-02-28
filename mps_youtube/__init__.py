import importlib.metadata

try:
    __version__ = importlib.metadata.version("yewtube")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unable to determine"

__author__ = "iamtalhaasghar"
__license__ = "GPLv3"
__url__ = "https://github.com/mps-youtube/yewtube"
