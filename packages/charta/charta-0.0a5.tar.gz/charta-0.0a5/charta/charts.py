import json


class JSONSerializable:

    def to_dict(self):
        raise NotImplementedError


class Series(JSONSerializable):

    def __init__(self, key, data):
        self.key = key
        self.data = data

    def to_dict(self):
        return {"type": "Series", "key": self.key, "data": list(self.data)}


class Chart(JSONSerializable):

    def __init__(self, key, series):
        self.key = key
        self.series = series

    def to_dict(self):
        return {"type": "Chart", "key": self.key, "series": self.series}
