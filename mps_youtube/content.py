import math

class Content:
    def getPage(self, page):
        max_results = screen.getxy().max_results
        s = page * max_results
        e = (page + 1) * max_results
        self.get_display

    def numPages(self):
        page_count = math.ceil(g.result_count/screen.getxy().max_results)


class SongList(Content):
    def __init__(songs, length=None, msg=None, failmsg=None, loadmsg=None):
        self.length = length
        if callable(func):
            self.songs, self.length = func(s, e)
        else:
            self.songs = func[s:e]
            if self.length is None:
                self.length = len(func)

        self.msg = msg
        self.failmsg = failmsg
        self.loadmsg = loadmsg

    def get_display(self, item, height, width):



def paginatesongs(func, page=0, splash=True, dumps=False,
        length=None, msg=None, failmsg=None, loadmsg=None):
    if splash:
        g.message = loadmsg or ''
        g.content = logo(col=c.b)
        screen.update()

    max_results = screen.getxy().max_results

    if dumps:
        s = 0
        e = None
    else:
        s = page * max_results
        e = (page + 1) * max_results

    if callable(func):
        songs, length = func(s, e)
    else:
        songs = func[s:e]
        if length is None:
            length = len(func)

    args = {'func':func, 'length':length, 'msg':msg,
            'failmsg':failmsg, 'loadmsg': loadmsg}
    g.last_search_query = (paginatesongs, args)
    g.browse_mode = "normal"
    g.current_page = page
    g.result_count = length
    g.model.songs = songs
    g.content = generate_songlist_display()
    g.last_opened = ""
    g.message = msg or ''
    if not songs:
        g.message = failmsg or g.message

    if songs:
        # preload first result url
        preload(songs[0], delay=0)

