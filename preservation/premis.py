"""Premis serialization from / to JSON and XML"""

import json


class EventJson(object):

    """Premis event serializer.

    TODO: this is only development stub.
    TODO: Replace this with proper Premis event serialization!

    """

    def __init__(self, event_record=None):
        """TODO: Docstring for __init__.

        :event_type: TODO
        :event_detail: TODO
        :returns: TODO

        """
        if type(event_record) == str:
            self.from_json(event_record)
        else:
            self.fields = event_record

    def from_json(self, json_fields):
        """TODO: Docstring for serialize.
        :returns: TODO

        """
        self.fields = json.loads(json_fields)

    def to_json(self):
        """TODO: Docstring for serialize.
        :returns: TODO

        """
        return json.dumps(self.fields)

    def __str__(self):
        """TODO: Docstring for __str__.
        :returns: TODO

        """
        return self.to_json()

    def __iter__(self):
        """TODO: Docstring for __next__.
        :returns: TODO

        """
        for line in self.to_json():
            yield line
