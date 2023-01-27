"""
    ContentQuery is an abstraction layer between the the pafy.call_gdata
    and the listViews.

    It lets you treat A query as a list of all the results, even though
    data is only queried when requested.
"""

from . import util, pafy


class ContentQuery:
    """ A wrapper for pafy.call_gdata. I lets you treat a search as a list,
        but the results will only be fetched when needed.
    """
    maxresults = 0
    pdata = []
    nextpagetoken = None

    datatype = None
    query = None
    api = None

    def __init__(self, datatype, api, query):
        # Perform initial API call, setBoundaries
        # call parseData

        self.datatype = datatype
        self.query = query
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
        # qry = dict(
        #     pageToken=self.nextpagetoken,
        #     **(self.query)
        #     ) if self.nextpagetoken else self.query

        # Run query
        util.dbg("CQ.query", self.query)
        data = pafy.channel_search(self.query)#pafy.call_gdata(self.api, qry)
        
        self.maxresults = len(data)#int(data.get("pageInfo").get("totalResults"))
        self.nextpagetoken = None#data.get("nextPageToken")

        for obj in data:
            self.pdata.append(self.datatype(obj))
