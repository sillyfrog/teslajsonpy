"""An example of streaming to allow a full implementation down the track"""

import base64
import websocket
import json

STREAM_API = "wss://streaming.vn.teslamotors.com/connect"

websocket.setdefaulttimeout(60)


class Stream:
    def __init__(self, email, vehicle):
        # XXX Need to keep the login email address on the Controller
        self._email = email
        self._vehicle = vehicle

    def start(self, on_message, on_error=None, on_close=None):
        """Start streaming for this vehicle

        on_message: A call back, with a single argument of the decoded JSON
            returned by the server.
        on_error: An optional callback called by the underlying websocket on
            error, arguments are the websocket and the error object
        on_close: An optional callback called by the underlying websocket when
            the connection is closed.
        """
        self._on_message = on_message
        encoded = base64.b64encode(
            "{}:{}".format(self._email, self._vehicle['tokens'][0]).encode("ascii")
        ).decode("ascii")
        header = "Authorization: Basic {}".format(encoded)
        # websocket.enableTrace(True)
        ws = websocket.WebSocketApp(
            "{}/{}".format(STREAM_API, self._vehicle['vehicle_id']),
            header=[header],
            on_message=self.ws_message,
            on_error=on_error,
            on_close=on_close,
        )
        ws.run_forever()

    def ws_message(self, msg):
        text = msg.decode()
        data = json.loads(text)
        self._on_message(data)
