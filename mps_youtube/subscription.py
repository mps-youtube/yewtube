import datetime


class Subscription(object):

    """ Representation of a subscription. """

    def __init__(self, userid=None, username=None):
        """ class members. """
        self.lastcheck = datetime.datetime.utcnow().isoformat("T") + "Z"
        self.userid = userid
        self.username = username


    def update(self):
        """ Update lastcheck. """
        self.lastcheck = datetime.datetime.utcnow().isoformat("T") + "Z"
