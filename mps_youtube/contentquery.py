"""
    ContentQuery is an abstraction layer between the the pafy.call_gdata
    and the listViews.

    It lets you treat A query as a list of all the results, even though
    data is only queried when requested.
"""

from . import util


class ContentQuery:
    """ A wrapper for pafy.call_gdata. I lets you treat a search as a list,
        but the results will only be fetched when needed.
    """
    maxresults = 0
    pdata = []
    nextpagetoken = None

    datatype = None
    queries = None
    api = None

    def __init__(self, datatype, api, qs):
        # Perform initial API call, setBoundaries
        # call parseData

        self.datatype = datatype
        self.queries = qs
        self.api = api

        self.pdata = []

        self._perform_api_call()

    def __getitem__(self, iid):
        # Check if we already got the item or slice needed
        # Call and parse nextPage as long as you dont have the data
        # needed.
        last_id = iid.stop if iid.__class__ == slice else iid
        last_datapoint = min(last_id, self.maxresults)
        while len(self.pdata) < last_datapoint:
            self._perform_api_call()
        return self.pdata[iid]

    def count(self):
        """ Returns how many items are in the list """
        return self.maxresults

    def __len__(self):
        return abs(self.count())

    def _perform_api_call(self):
        # Include nextPageToken if it is set
        qry = dict(
            pageToken=self.nextpagetoken,
            **(self.queries)
            ) if self.nextpagetoken else self.queries

        # Run query
        util.dbg("CQ.query", qry)
        data = None#pafy.call_gdata(self.api, qry)
        
        self.maxresults = int(data.get("pageInfo").get("totalResults"))
        self.nextpagetoken = data.get("nextPageToken")

        for obj in data.get("items"):
            self.pdata.append(self.datatype(obj))
