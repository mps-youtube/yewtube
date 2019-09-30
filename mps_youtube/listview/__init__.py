"""
    DOCSTING COMES HERE
"""
import re
import math

from .. import c, g, util, content
from .base import ListViewItem
from .user import ListUser
from .livestream import ListLiveStream
from .songtitle import ListSongtitle


class ListView(content.PaginatedContent):
    """ Content Agnostic Numbered List

        This class, using ListViewItems as abstractions you can
        give it a list of data and which columns to show and it will
        show it.

        Todo:
            Currently we rely on the commands/play code to send information
            about which elements are being picked.

        Attributes:
            func        The function that will be run on the selected items
            objects     List of objects(or a ContentQuery object)
            columns     A list of Hashes containing information about which
                        columns to show
            page        Current Page

        Column format:
            {"name": "idx", "size": 3, "heading": "Num"}
            name:    The method name that will be called from the ListViewItem
            size:    How much size is allocated to the columns,
                     see ListView.content for more information about
                     the dynamic options
            heading: The text shown in the header

            "idx" is generated in the content function, not by the ListViewItem
    """
    func = None
    objects = None
    columns = None
    page = 0

    def __init__(self, columns, objects, function_call=None):
        """ """
        self.func = function_call
        self.objects = objects
        self.columns = columns
        self.object_type = None

        # Ensure single type of object
        types = len(set([obj.__class__ for obj in objects]))
        if types == 0:
            raise BaseException("No objects in list")
        if types > 1:
            raise BaseException("More than one kind of objects in list")

        self.object_type = [obj.__class__ for obj in objects][0]

    def numPages(self):
        """ Returns # of pages """
        return max(1, math.ceil(len(self.objects) / self.views_per_page()))

    def getPage(self, page):
        self.page = page
        return self.content()

    def _page_slice(self):
        chgt = self.views_per_page()
        return slice(self.page * chgt, (self.page+1) * chgt)

    def content(self):
        """ Generates content

            ===============
            Dynamic fields
            ===============

            Column.size may instead of an integer be a string
            containing either "length" or "remaining".

            Length is for time formats like 20:40
            Remaining will allocate all remaining space to that
            column.

            TODO: Make it so set columns can set "remaining" ?
        """
        # Sums all ints, deal with strings later
        remaining = (util.getxy().width) - sum(1 + (x['size'] if x['size'] and x['size'].__class__ == int else 0) for x in self.columns) - (len(self.columns))
        lengthsize = 0
        if "length" in [x['size'] for x in self.columns]:
            max_l = max((getattr(x, "length")() for x in self.objects))
            lengthsize = 8 if max_l > 35999 else 7
            lengthsize = 6 if max_l < 6000 else lengthsize

        for col in self.columns:
            if col['size'] == "remaining":
                col['size'] = remaining - lengthsize
            if col['size'] == "length":
                col['size'] = lengthsize

        for num, column in enumerate(self.columns):
            column['idx'] = num
            column['sign'] = "-" if not column['name'] == "length" else ""

        fmt = ["%{}{}s  ".format(x['sign'], x['size']) for x in self.columns]
        fmtrow = fmt[0:1] + ["%s  "] + fmt[2:]
        fmt, fmtrow = "".join(fmt).strip(), "".join(fmtrow).strip()
        titles = tuple([x['heading'][:x['size']] for x in self.columns])
        out = "\n" + (c.ul + fmt % titles + c.w) + "\n"

        for num, obj in enumerate(self.objects[self._page_slice()]):
            col = (c.r if num % 2 == 0 else c.p)
            idx = num + (self.views_per_page() * self.page) + 1

            line = ''
            for column in self.columns:
                fieldsize, field = column['size'], column['name']
                direction = "<" if column['sign'] == "-" else ">"

                if field == "idx":
                    field = "%2d" % idx

                else:
                    field = getattr(obj, field)(fieldsize)
                    field = str(field) if field.__class__ != str else field

                line += util.uea_pad(fieldsize, field, direction)

                if column != self.columns[-1]:
                    line += "  "

            line = col + line + c.w
            out += line + "\n"
        
        return out

    def _play(self, _, choice, __):  # pre, choice, post
        """ Handles what happends when a user selects something from the list
            Currently this functions hooks into commands/play
        """

        uids = []
        for splitted_choice in choice.split(","):
            cho = splitted_choice.strip()
            if cho.isdigit():
                uids.append(int(cho) - 1)
            else:
                cho = cho.split("-")
                if cho[0].isdigit() and cho[1].isdigit():
                    uids += list(range(int(cho[0]) - 1, int(cho[1])))

        var = getattr(self.object_type, "return_field")()
        self.func([getattr(self.objects[x], var)() for x in uids])

    def views_per_page(self):
        """ Determines how many views can be per page
        """
        return util.getxy().max_results
