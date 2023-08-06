import json
import pathlib
import os
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.httpserver
import zmq
from zmq.eventloop import zmqstream

from charta.common import DEFAULT_WEB_PORT, DEFAULT_ZMQ_PORT


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    """
    A simple class to handle WebSockets. Tracks all open WebSockets and provides
    a static method ofor sending a message to all clients.
    """

    clients = []

    def check_origin(self, origin):
        return True

    def open(self):
        print("connection established")
        WebSocketHandler.clients.append(self)

    def on_message(self, message):
        data = json.loads(message)
        method = data["method"]
        if method == "save":
            try:
                print("Saving data to {}".format(data["filename"]))
                with open(data["filename"], "w") as f:
                    f.write(data["data"])
            except Exception as e:
                print(repr(e))
        else:
            print("Unknown method: {}".format(method))

    def on_close(self):
        WebSocketHandler.clients.remove(self)
        print("connection closed")

    @staticmethod
    def write_messages(msg):
        for c in WebSocketHandler.clients:
            try:
                c.write_message(msg)
            except (tornado.websocket.WebSocketClosedError):
                c.on_close()


def handle_zmq_message(stream, msg):
    """
    A simple message handler that forwards messages from a ZMQSocket to a WebSocketHandler.
    """
    for m in msg:
        data = json.loads(m)
        WebSocketHandler.write_messages(m)

    stream.send(b"ok")


def setup_client(app, port=DEFAULT_ZMQ_PORT):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.connect("{protocol}://{host}:{port}".format(protocol="tcp",
        host="localhost",
        port=port))
    print("zmq port: {port}".format(port=port))
    stream = zmqstream.ZMQStream(socket)
    stream.on_recv_stream(handle_zmq_message)


root = pathlib.Path(__file__).parent.absolute()


def make_app():
    app = tornado.web.Application([
        (r"/websocket", WebSocketHandler),
        (r"/(.*)", tornado.web.StaticFileHandler, {
            "path": os.path.join(root, "static"),
            "default_filename": "index.html"
            }),
        ])
    return app


def try_listen(app, port_range):
    assert len(port_range) > 0, "Argument port_range must have non-zero length."
    error = None
    for port in port_range:
        try:
            app.listen(port)
            print("web port: {}".format(port))
            print(f"http://localhost:{port}")
            return port
        except OSError as e:
            error = e
    raise error

