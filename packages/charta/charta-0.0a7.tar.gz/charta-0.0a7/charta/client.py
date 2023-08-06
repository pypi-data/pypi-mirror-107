import zmq
import time

from charta.common import DEFAULT_ZMQ_PORT

def send_data(method, protocol="tcp", port=DEFAULT_ZMQ_PORT, **kwargs):
    with zmq.Context().socket(zmq.REQ) as socket:
        socket.bind("tcp://*:{port}".format(protocol=protocol, port=port))
        kwargs["method"] = method
        socket.send_json(kwargs)


class Dashboard:
    _default = None

    @classmethod
    def default(cls):
        if cls._default is None:
            cls._default = cls()
        return cls._default

    def __init__(self, port=DEFAULT_ZMQ_PORT):
        self.port = port

    def send_data(self, *args, **kwargs):
        send_data(*args, port=self.port, **kwargs)

    def add_chart(self, chart):
        if (type(chart) == list):
            self.send_data("create_chart", data=[c.to_dict() for c in chart])
        else:
            self.send_data("create_chart", data=chart.to_dict())

    def add_series(self, series):
        if (type(series) == list):
            self.send_data("create_series", data=[s.to_dict() for s in series])
        else:
            self.send_data("create_series", data=series.to_dict())

    def append_series(self, series_key, data):
        self.extend_series(series_key, [data])

    def extend_series(self, series_key, data):
        self.send_data("extend_series", data=list(data), key=series_key)

    def save(self, filename):
        self.send_data("read", filename=filename)

    def update(self):
        self.send_data("update")

    def reset(self):
        self.delete_series()
        self.delete_charts()

    def delete_charts(self):
        self.send_data("delete_charts")

    def delete_series(self):
        self.send_data("delete_series")

