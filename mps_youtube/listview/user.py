from .base import ListViewItem
from .. import util as u

class ListUser(ListViewItem):
    """ Describes a user
    """
    # pylint: disable=unused-argument
    def id(self, length=0):
        """ Returns YTID """
        return self.data.get("id")

    def name(self, length=10):
        """ Returns channel name """
        return u.uea_pad(length, self.data.get("title"))

    def description(self, length=10):
        """ Channel description"""
        return u.uea_pad(length, self.data["descriptionSnippet"][0]['text'] if self.data['descriptionSnippet'] is not None else 'No description found')

    def kind(self, length=10):
        """ Returns the youtube datatype
            Example: youtube#channel, youtube#video
        """
        return self.data.get("type")

    def ret(self):
        """ Used in the ListView play function """
        return (self.name(), self.id(), "")

    @staticmethod
    def return_field():
        """ Determines which function will be called on selected items """
        return "ret"
