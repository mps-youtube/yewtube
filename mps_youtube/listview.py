"""
    DOCSTING COMES HERE
"""
import re

from . import c, util, content


class ListViewItem(object):
    """ TODO
    """
    data = None

    def __init__(self, data):
        self.data = data

    def __getattr__(self, key):
        return self.data[key] if key in self.data.keys() else None

    def length(self, _):
        """ Returns length of ListViewItem
            A LVI has to return something for length
            even if the item does not have one.
        """
        return 0


class ListUser(ListViewItem):
    """ Describes a user
    """
    # pylint: disable=unused-argument
    def id(self, length=0):
        """ Returns YTID """
        return self.data.get("id").get("channelId")

    def name(self, length=10):
        """ Returns channel name """
        return util.uea_pad(length, self.data.get("snippet").get("title"))

    def description(self, length=10):
        """ Channel description"""
        return util.uea_pad(length, self.data.get("snippet").get("description"))

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


class ListView(content.Content):
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
        del types

    def pages(self):
        """ Returns # of pages """
        items = len(self.objects) / self.views_per_page()
        ret = 0
        while items > 0:
            ret += 1
            items -= 1
        return ret

    def _page_slice(self):
        chgt = self.views_per_page()
        return slice(self.page * chgt, (self.page+1) * chgt)

    def has_next_page(self):
        """ Returns True if this is not the last page """
        return self.page + 1 <= self.pages()

    def has_previous_page(self):
        """ Returns True if this page is not the first one """
        return self.page > 0

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
        remaining = (util.getxy().width - 2) - sum(1 + (x['size'] if x['size'] and x['size'].__class__ == int else 0) for x in self.columns)
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

            data = []
            for column in self.columns:
                fieldsize, field = column['size'], column['name']
                if field == "idx":
                    data.append("%2d" % (num + (self.views_per_page() * self.page) + 1))
                else:
                    field = getattr(obj, field)(fieldsize)
                    if len(field) > fieldsize:
                        field = field[:fieldsize]
                    else:
                        field = field + (" " * (fieldsize - len(field)))
                    data.append(field)
            line = col + (fmtrow % tuple(data)) + c.w
            out += line + "\n"
        
        # Page number
        pagenum = ""
        pagenum += "<" if self.has_previous_page() else "["
        pagenum += str(self.page + 1) + "/" + str(self.pages() + 1)
        pagenum += ">" if self.has_next_page() else "]"
        out += (" " * (util.getxy().width - len(pagenum))) + pagenum + "\n"
        return out

    def run(self, str_):
        """ Allows a ListView to have its own commands it responds to

            Returns True if it found a suitable command, should stop
            further matching.

        """

        def goto_next_page(obj, _):
            """ Increase self.page by 1 """
            obj.page = obj.page + 1 if obj.has_next_page() else obj.page

        def goto_prev_page(obj, _):
            """ Decrease Page by 1 """
            obj.page = obj.page - 1 if obj.has_previous_page() else obj.page

        commands = [
            {"cmd": r"^n", "func": goto_next_page},
            {"cmd": r"^p", "func": goto_prev_page}
        ]

        for cobj in commands:
            if re.match(cobj['cmd'], str_):
                cobj['func'](self, str_)
                return True

        return False

    def _play(self, _, choice, __):  # pre, choice, post
        """ Handles what happends when a user selects something from the list
            Currently this functions hooks into commands/play
        """
        uid = int(choice.split(",")[0].strip()) - 1
        attr = getattr(self.objects[uid],
                       self.objects.datatype.return_field(), None)

        return self.func(attr())

    def views_per_page(self):
        """ Determines how many views can be per page
        """
        return util.getxy().height - 6
