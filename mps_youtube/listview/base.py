class ListViewItem:
    """Base class for items
    Used by Listview
    """

    data = None

    def __init__(self, data):
        self.data = data

    def __getattr__(self, key):
        return self.data[key] if key in self.data.keys() else None

    def length(self, _=0):
        """Returns length of ListViewItem
        A LVI has to return something for length
        even if the item does not have one.
        """
        return 0
