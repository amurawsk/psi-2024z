import socket
import sys


BUFSIZE = 4096


def start_server(host='pserver', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    print(f"Serwer nasłuchuje na {host}:{port}")

    while True:
        data, address = server_socket.recvfrom(BUFSIZE)
        length = int.from_bytes(data[:2], byteorder='big')
        content = data[2:]

        if len(content) == length:
            if all(c == b'A'[0] + (i % 26) for i, c in enumerate(content)):
                print(f"Odebrano poprawny datagram od {address} o rozmiarze {len(data)} bajtów")
                server_socket.sendto(b"OK", address)
            else:
                print(f"Odebrano błędny datagram od {address} - dane uległy zmianie")
        else:
            print(f"Odebrano błędny datagram od {address} - [({len(content)=}) != ({length=})]")


if __name__ == "__main__":
    start_server(port=int(sys.argv[1]))
