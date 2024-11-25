import socket
import sys


BUFSIZE = 4096


def start_server(host='pserver', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    print(f"Serwer nasłuchuje na {host}:{port}")
    
    expected_sequence_bit = 0

    while True:
        data, address = server_socket.recvfrom(BUFSIZE)
        sequence_bit = data[0]
        length = int.from_bytes(data[1:3], byteorder='big')
        content = data[3:]
        
        if sequence_bit != expected_sequence_bit:
            print(f"Nieoczekiwany bit sekwencyjny {sequence_bit} (oczekiwano {expected_sequence_bit}). Odrzucono.")
            server_socket.sendto(bytes([1 - expected_sequence_bit]) + b"ACK",  address)
            continue

        if len(content) == length:
            if all(c == b'A'[0] + (i % 26) for i, c in enumerate(content)):
                print(f"Odebrano poprawny datagram od {address} o rozmiarze wiadomości {len(content)}B (cały datagram {len(content)+2}B)")
                server_socket.sendto(bytes([sequence_bit]) + b"ACK", address)
                expected_sequence_bit = 1 - expected_sequence_bit
            else:
                print(f"Odebrano błędny datagram od {address} - dane uległy zmianie")
                server_socket.sendto(bytes([1 - expected_sequence_bit]) + b"Zle dane", address)
        else:
            print(f"Odebrano błędny datagram od {address} - [({len(content)=})B != ({length=})B]")
            server_socket.sendto(bytes([1 - expected_sequence_bit]) + b"Odebrano niepoprawna dlugosc datagramu", address)


if __name__ == "__main__":
    start_server(port=int(sys.argv[1]))
