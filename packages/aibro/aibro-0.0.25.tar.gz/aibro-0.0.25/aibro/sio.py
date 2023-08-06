from time import sleep

import socketio

sio = socketio.Client()


@sio.event
def connect():
    pass
    # print("connection established")


@sio.on("to_client")
def to_client(data):
    print(data)


@sio.event
def disconnect():
    pass
    # print("disconnected from server")
    # TODO make an API call to tell that the server has disconnected


def sio_disconnect():
    if sio.connected:
        sio.disconnect()


def connect_to_server_socket(public_ip: str, port: str = "12345"):
    if sio.connected:
        sio.disconnect()

    sleep(1)
    retries = 3
    while retries > 0:
        try:
            sio.connect(f"http://{public_ip}:{port}/", wait=True)
            break
        except Exception as e:
            print(f"{str(e)}")
            print("wait for 5s then retry")
            sleep(5)
            retries -= 1

    if not retries:
        raise Exception(f"Failed to connect to server socket {public_ip}")
