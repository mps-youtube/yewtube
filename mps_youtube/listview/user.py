from .base import ListViewItem
from .. import util as u

class ListUser(ListViewItem):
    """ Describes a user
    """
    # pylint: disable=unused-argument
    def id(self, length=0):
        """ Returns YTID """
        return self.data.get("id").get("channelId")

    def name(self, length=10):
        """ Returns channel name """
        return u.uea_pad(length, self.data.get("snippet").get("title"))

    def description(self, length=10):
        """ Channel description"""
        return u.uea_pad(length, self.data.get("snippet").get("description"))

    def kind(self, length=10):
        """ Returns the youtube datatype
            Example: youtube#channel, youtube#video
        """
        return self.data.get("id").get("kind")

    def ret(self):
        """ Used in the ListView play function """
        return (self.data.get("snippet").get("title"), self.id(), "")

    @staticmethod
    def return_field():
        """ Determines which function will be called on selected items """
        return "ret"
