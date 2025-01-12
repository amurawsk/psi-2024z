import socket
import threading
import hashlib
import random

import crypto_utils

clients = {}
threads = {}
stop_threads = {}
lock = threading.Lock()


def establish_connection(client_socket):
    response = client_socket.recv(1024).decode("utf-8")
    if response[:11] != "ClientHello":
        raise ValueError(response)
    A, p, g = response[11:].split(",")
    A, p, g = int(A), int(p), int(g)
    b = random.randint(1, 100)
    s = (A**b) % p

    B = (g**b) % p
    data_to_send = f"ServerHello{B}"
    client_socket.send(data_to_send.encode("utf-8"))
    return s


def handle_client(client_socket, client_address, timeout_event):
    with lock:
        clients[client_address] = client_socket
        stop_threads[client_address] = False

    shared_key = establish_connection(client_socket)
    aes_key = hashlib.sha256(str(shared_key).encode()).digest()
    print(f"\n[INFO] Klient {client_address} połączony.")
    print(f"[DEBUG] Secrets - {shared_key=}, {aes_key=}")

    try:
        while True:
            with lock:
                if stop_threads[client_address]:
                    break
            try:
                if timeout_event.is_set():
                    break
                encrypted_data = client_socket.recv(1024)
                print(f'[DEBUG] Received - {encrypted_data=}')
                decrypted_message = crypto_utils.get_decrypted_message(
                    aes_key, encrypted_data, shared_key
                )
                print(f"Od: [{client_address}]: {decrypted_message=}")
                if decrypted_message == 'EndSessionC':
                    print(f"[INFO] Klient {client_address} zakończył połączenie.")
                    break

                message = 'Wiadomość odebrana!'
                encrypted_message = crypto_utils.get_encrypted_message(
                    aes_key, message, shared_key
                )
                print(f'[DEBUG] Sent - {encrypted_message=}')
                client_socket.send(encrypted_message)
            except socket.timeout:
                continue
            except OSError:
                print(f"[INFO] OS ERROR.")
    except ConnectionResetError:
        print(f"[INFO] Klient {client_address} zakończył połączenie.")
    finally:
        with lock:
            if client_address in clients:
                del clients[client_address]
            if client_address in threads:
                del threads[client_address]
            if client_address in stop_threads:
                del stop_threads[client_address]
        client_socket.close()
        print(f"[INFO] Połączenie z {client_address} zakończone.")


def server_commands():
    while True:
        print("\nDostępne opcje:")
        print("1. Wyświetl listę klientów")
        print("2. Zakończ połączenie z klientem")
        print("3. Zamknij serwer")
        option = input("Wybierz opcję: ")

        if option == "1":
            print("\n[INFO] Lista aktywnych klientów:")
            with lock:
                for idx, address in enumerate(clients.keys()):
                    print(f"{idx + 1}. {address}")
        elif option == "2":
            print("\n[INFO] Lista klientów:")
            with lock:
                addresses = list(clients.keys())
            for idx, address in enumerate(addresses):
                print(f"{idx + 1}. {address}")
            try:
                client_idx = int(input("Podaj numer klienta do rozłączenia: ")) - 1
                if 0 <= client_idx < len(addresses):
                    client_to_disconnect = addresses[client_idx]
                    with lock:
                        stop_threads[client_to_disconnect] = True
                    threads[client_to_disconnect].join(timeout=2)
                    print(f"[INFO] Rozłączono klienta {client_to_disconnect}.")
                else:
                    print("[BŁĄD] Nieprawidłowy numer klienta.")
            except ValueError:
                print("[BŁĄD] Wprowadź poprawny numer.")
        elif option == "3":
            print("[INFO] Zamykam serwer...")
            with lock:
                for address in list(clients.keys()):
                    stop_threads[address] = True
            for thread in list(threads.values()):
                thread.join(timeout=2)
            with lock:
                clients.clear()
                threads.clear()
                stop_threads.clear()
            break
        else:
            print("[BŁĄD] Nieznana opcja!")


def start_server(host="127.0.0.1", port=12345, max_clients=5):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((host, port))
        server.listen(max_clients)
        print(f"[INFO] Serwer uruchomiony na {host}:{port}")
        threading.Thread(target=server_commands, daemon=True).start()
        try:
            while True:
                client_socket, client_address = server.accept()
                client_socket.settimeout(1.0)

                timeout_event = threading.Event()
                client_thread = threading.Thread(
                    target=handle_client,
                    args=(client_socket, client_address, timeout_event),
                    daemon=True,
                )
                with lock:
                    threads[client_address] = client_thread
                client_thread.start()
        except KeyboardInterrupt:
            print("\n[INFO] Zamykanie serwera...")
            with lock:
                for address in list(clients.keys()):
                    stop_threads[address] = True
            for thread in list(threads.values()):
                thread.join(timeout=2)
            with lock:
                clients.clear()
                threads.clear()
                stop_threads.clear()
            print("[INFO] Serwer zamknięty.")


if __name__ == "__main__":
    start_server()
