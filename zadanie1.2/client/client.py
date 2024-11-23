import socket
import time
import sys


NUM_DGRAMS = 10


def start_client(host='localhost', port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    size = 512
    sequence_bit = 0
    
    for i in range(NUM_DGRAMS):
        repeat = True
        while repeat:
            length = (size).to_bytes(2, byteorder='big')
            content = bytes([(65 + (i % 26)) for i in range(size)])
            message = bytes([sequence_bit]) + length + content

            print(f"Wysyłanie wiadomości nr {i} - rozmiar wiadomości {size}B (całego datagramu {size+2}B)...")
            client_socket.sendto(message, (host, port))

            try:
                client_socket.settimeout(2)
                response, _ = client_socket.recvfrom(128)
                ack_bit = response[0]
                # response_message = response[1:]
                if ack_bit == sequence_bit:
                    print(f"Otrzymano potwierdzenie dla wiadomości o rozmiarze {size}B (całego datagramu {size+2}B)")
                    sequence_bit = 1 - sequence_bit # zamiana wartosci bitu
                    repeat = False
                else:
                    print(f"Brak potwierdzenia dla wiadomości o rozmiarze {size}B (całego datagramu {size+2}B) - retransmisja...")
            except socket.timeout:
                print(f"Timeout potwierdzenia dla wiadomości o rozmiarze {size}B (całego datagramu {size+2}B) - retransmisja...")
            print()
            time.sleep(1)


if __name__ == "__main__":
    start_client(sys.argv[1], int(sys.argv[2]))
