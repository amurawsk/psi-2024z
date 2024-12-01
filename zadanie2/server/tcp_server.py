import socket
import struct

HOST = '127.0.0.1'
PORT = 12345

def deserialize_tree(data):
    offset = 0
    nodes = []

    while offset < len(data):
        data_16 = struct.unpack('!H', data[offset:offset + 2])[0]
        data_32 = struct.unpack('!I', data[offset + 2:offset + 6])[0]
        text = data[offset + 6:offset + 26].decode('utf-8').strip('\x00')
        nodes.append((data_16, data_32, text))
        offset += 26

    return nodes

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")

    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        data = conn.recv(1024)
        if data:
            nodes = deserialize_tree(data)
            for node in nodes:
                print(f"Node: 16-bit: {node[0]}, 32-bit: {node[1]}, Text: '{node[2]}'")

