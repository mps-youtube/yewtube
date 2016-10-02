import re

from .. import g, c, playlists, content, util
from ..subscription import Subscription
from . import search, command, WORD


@command(r'unsub\s*(%s)' % WORD)
def unsub(name):
    """ Remove subscription by user name.  Get closest name match. """
    ret = search.channelfromname(name)

    if not ret: # Error
        g.message = util.F('user not found')
        return
    user, id = ret

    sub = subscription_by_id(id)
    if not sub:
        g.message = util.F('user not followed')
        return

    g.usersubs.remove(sub)
    playlists.save()

    g.content = content.generate_subscriptions_display()
    g.message = util.F('sub help')


@command(r'sub\s+(%s)' % WORD)
def sub(name):
    """ Add subscription by user name.  Get closest name match. """
    ret = search.channelfromname(name)
    if not ret: # Error
        g.message = util.F('user not found')
        return

    user, id = ret
    if subscription_by_id(id):
        g.message = util.F('user already followed')
        return

    g.usersubs.append(Subscription(id, user))
    playlists.save()

    g.content = content.generate_subscriptions_display()
    g.message = util.F('sub help')


def subscription_by_id(id):
    """ Return subscription from id. """
    for sub in g.usersubs:
        if sub.userid == id:
            return sub

    return

def update(id):
    """ Update lastcheck if subscription exists. """
    sub = subscription_by_id(id)
    if sub:
        sub.update();
        playlists.save()

    return

@command(r'subs')
def subs():
    """ List user saved subscriptions (or display pls). """
    if not g.usersubs:
        g.message = util.F('no subscriptions')
        g.content = g.content or \
                content.generate_songlist_display(zeromsg=g.message)

    else:
        g.content = content.generate_subscriptions_display()
        g.message = util.F('sub help')
