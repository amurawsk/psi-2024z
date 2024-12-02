from node import TEXTFIELD_SIZE, deserialize_tree
import socket
import sys


BUFFER_SIZE = TEXTFIELD_SIZE*3 + 1000


def start_server(host='pserver', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 151 * 1024)
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")

        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            data = conn.recv(BUFFER_SIZE)
            print(f'Received data length: {len(data)}B')
            if data:
                node = deserialize_tree(data)
                print('\nReceived tree data:')
                print(f'{len(node.text)=}')
                print(f'{len(node.left.text)=}')
                print(f'{len(node.right.text)=}')


if __name__ == "__main__":
    start_server(port=int(sys.argv[1]))
