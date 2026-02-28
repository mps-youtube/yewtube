from .base import ListViewItem
from .. import util


class ListLiveStream(ListViewItem):
    """Class exposing necessary components of a live stream"""

    # pylint: disable=unused-argument
    def ytid(self, lngt=10):
        """Exposes ytid(string)"""
        return self.data.get("id").get("videoId")

    def ret(self):
        """Returns content.video compatible tuple"""
        return (self.ytid(), self.title(), self.length())

    def title(self, lngt=10):
        """exposes title"""
        return util.uea_pad(lngt, self.data.get("snippet").get("title"))

    def description(self, lngt=10):
        """exposes description"""
        return util.uea_pad(lngt, self.data.get("snippet").get("description"))

    @staticmethod
    def return_field():
        """ret"""
        return "ret"
