import math

from . import g, screen, c

# In the future, this could support more advanced features
class Content:
    pass


class PaginatedContent(Content):
    def getPage(self, page):
        raise NotImplementedError

    def numPages(self):
        raise NotImplementedError


class LineContent(PaginatedContent):
    def getPage(self, page):
        max_results = screen.getxy().max_results
        s = page * max_results
        e = (page + 1) * max_results
        return self.get_text(s, e)

    def numPages(self):
        return math.ceil(self.get_count()/screen.getxy().max_results)

    def get_text(self, s, e):
        raise NotImplementedError

    def get_count(self):
        raise NotImplementedError


class StringContent(LineContent):
    def __init__(self, string):
        self._lines = string.splitlines()

    def get_text(self, s, e):
        return '\n'.join(self._lines[s:e])

    def get_count(self):
        width = screen.getxy().width
        count = sum(len(i) // width + 1 for i in self._lines)
        return count


def page_msg(page=0):
    """ Format information about currently displayed page to a string. """
    if isinstance(g.content, PaginatedContent):
        page_count = g.content.numPages()
    else:
        page_count = math.ceil(g.result_count/screen.getxy().max_results)

    if page_count > 1:
        pagemsg = "{}{}/{}{}"
        #start_index = max_results * g.current_page
        return pagemsg.format('<' if page > 0 else '[',
                              "%s%s%s" % (c.y, page+1, c.w),
                              page_count,
                              '>' if page + 1 < page_count else ']')
    return None
