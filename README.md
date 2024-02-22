# StompyPy <img src="https://github.com/hugobrilhante/stomppy/blob/main/docs/images/stompypy.png" width=35 height=35 />

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=hugobrilhante_stompypy&metric=alert_status)](https://sonarcloud.io/dashboard?id=hugobrilhante_stompypy)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=hugobrilhante_stompypy&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=hugobrilhante_stompypy)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=hugobrilhante_stompypy&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=hugobrilhante_stompypy)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=hugobrilhante_stompypy&metric=security_rating)](https://sonarcloud.io/dashboard?id=hugobrilhante_stompypy)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=hugobrilhante_stompypy&metric=bugs)](https://sonarcloud.io/dashboard?id=hugobrilhante_stompypy)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=hugobrilhante_stompypy&metric=code_smells)](https://sonarcloud.io/dashboard?id=hugobrilhante_stompypy)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=hugobrilhante_stompypy&metric=vulnerabilities)](https://sonarcloud.io/dashboard?id=hugobrilhante_stompypy)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=hugobrilhante_stompypy&metric=ncloc)](https://sonarcloud.io/dashboard?id=hugobrilhante_stompypy)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=hugobrilhante_stompypy&metric=coverage)](https://sonarcloud.io/summary/new_code?id=hugobrilhante_stompypy)
[![PyPI version](https://badge.fury.io/py/stompypy.svg)](https://badge.fury.io/py/stompypy)
[![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/https://github.com/hugobrilhante/stompypy/blob/main/LICENSE)
[![Downloads](https://pepy.tech/badge/stompypy/week)](https://pepy.tech/project/stompypy/week)

The stompypy is a simple implementation of the STOMP (Simple Text Oriented Messaging Protocol) protocol. It provides an easy way to connect to and exchange STOMP frames with a STOMP server.

## Installation

To install the stompypy package, you can use pip:

```shell
pip install stompypy
```

## Usage Example 🚀

Here's an example demonstrating how to use the `Stomp` class to interact with a STOMP server:

```python
import time

from stompypy import Listener
from stompypy import Stomp


class MyListener(Listener):
    def on_disconnect(self):
        print('Disconnected')

    def on_connect(self):
        print('Connected')

    def on_message(self, frame) -> None:
        print('Message:', frame.body)


if __name__ == '__main__':
    # Create a STOMP connection to the server
    connection = Stomp.create_connection(host='localhost', port=61613)

    # Add listener
    connection.add_listener(MyListener())

    # Connect to the STOMP server
    connection.connect()

    # Subscribe to a destination
    connection.subscribe(id='1', destination='/queue/example', ack_mode='auto')

    # Send a message to the destination
    connection.send(destination='/queue/example', content_type='text/plain', body=f'Hello World!')

    time.sleep(1)

    # Disconnect from the server
    connection.disconnect()
```

## Methods of the Stomp Class 🛠️

- `ack(message_id: str, transaction: Optional[str] = None) -> None`: Sends an ACKNOWLEDGE command to confirm receipt of a message.
- `abort(transaction: str) -> None`: Sends an ABORT command to roll back a transaction.
- `begin(transaction: str) -> None`: Sends a BEGIN command to start a transaction.
- `commit(transaction: str) -> None`: Sends a COMMIT command to confirm a transaction.
- `connect(host: Optional[str] = '/', accept_version: str = '1.2', login: Optional[str] = None, passcode: Optional[str] = None, heart_beat: Optional[Tuple[int, int]] = (0, 0)) -> None`: Connects to the STOMP server with the provided options.
- `disconnect(receipt_id: Optional[str] = None) -> None`: Disconnects from the STOMP server.
- `nack(message_id: str, transaction: Optional[str] = None) -> None`: Sends a NEGATIVE ACKNOWLEDGE command to deny receipt of a message.
- `send(destination: str, content_type: str, body: str, transaction: Optional[str] = None) -> None`: Sends a message to the specified destination.
- `subscribe(id: str, destination: str, ack_mode: str) -> None`: Subscribes to a destination with the specified ACKNOWLEDGE mode.
- `unsubscribe(id: str) -> None`: Unsubscribes from a destination.

For more information about the STOMP protocol, refer to the [STOMP 1.2 Specification](https://stomp.github.io/stomp-specification-1.2.html).
```
