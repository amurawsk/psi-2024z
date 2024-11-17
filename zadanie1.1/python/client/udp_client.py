import socket
import time
import sys


def start_client(host='localhost', port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sizes = [1, 100, 200, 500, 1000, 2000, 4000]
    # sizes = list(range(4090, 4100, 1)) # nie zadziała poprawnie dla wartości większych niż 4096 - bo taki rozmiar bufora w serwerze
    # sizes = list(range(65500, 65510)) # nie zostanie obsłużone - bo system nie obsługuje wiadomości powyżej 65507 bajtów

    for size in sizes:
        length = (max(size-2, 0)).to_bytes(2, byteorder='big') # 2 pierwsze bajty na rozmiar treści
        content = bytes([(65 + (i % 26)) for i in range(size-2)]) # stworzenie wiadomości
        message = length + content

        print(f"Wysyłanie wiadomości - rozmiar zawartości {size} bajtów...")
        client_socket.sendto(message, (host, port))

        try:
            client_socket.settimeout(1)
            response, _ = client_socket.recvfrom(128)
            if response == b"OK":
                print(f"Otrzymano potwierdzenie dla datagramu o rozmiarze {size} bajtów")
            else:
                print(response.decode('utf-8'))
        except socket.timeout:
            print("Brak odpowiedzi")
            break

        time.sleep(1)

if __name__ == "__main__":
    start_client(sys.argv[1], int(sys.argv[2]))
