from pip._vendor import pkg_resources

__version__ = next((p.version for p in pkg_resources.working_set if p.project_name.lower() == 'yewtube'), "unable to determine")
__author__ = "iamtalhaasghar"
__license__ = "GPLv3"
__url__ = "https://github.com/iamtalhaasghar/yewtube"

