import socket
import threading
import sys
import hashlib
import random

import crypto_utils

stop_client = False
p = 23
g = 5


def establish_connection(client_socket):
    a = random.randint(1, 100)
    A = (g**a) % p
    data_to_send = f"ClientHello{A},{p},{g}"
    client_socket.send(data_to_send.encode("utf-8"))

    response = client_socket.recv(1024).decode("utf-8")
    if response[:11] != "ServerHello":
        raise ValueError(response)
    B = int(response[11:])
    s = (B**a) % p
    return s


def receive_messages(client_socket, aes_key, shared_key):
    global stop_client
    try:
        while not stop_client:
            encrypted_data = client_socket.recv(1024)
            print(f'[DEBUG] Received - {encrypted_data=}')
            decrypted_message = crypto_utils.get_decrypted_message(
                aes_key, encrypted_data, shared_key
            )
            # if not response:
            #     print("[INFO] Serwer zakończył połączenie.")
            #     stop_client = True
            #     break
            print(f"Serwer: {decrypted_message=}")
    except ConnectionResetError:
        print("[INFO] Serwer wymusił zakończenie połączenia.")
    except OSError:
        print("[INFO] Połączenie z serwerem zostało przerwane.")
    finally:
        stop_client = True
        print("[INFO] Połączenie zakończone.")


def start_client(server_host="127.0.0.1", server_port=12345):
    global stop_client
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((server_host, server_port))

            shared_key = establish_connection(client_socket)
            aes_key = hashlib.sha256(str(shared_key).encode()).digest()

            print(f"[INFO] Połączono z serwerem {server_host}:{server_port}")
            print(f"[DEBUG] Secrets - {shared_key=}, {aes_key=}")

            threading.Thread(
                target=receive_messages, args=(client_socket, aes_key, shared_key,), daemon=True
            ).start()

            while not stop_client:
                try:
                    message = input("Message: ")
                    if stop_client:
                        break
                    if message.lower() == "exit":
                        print("[INFO] Rozłączanie...")
                        stop_client = True
                        break
                    encrypted_message = crypto_utils.get_encrypted_message(
                        aes_key, message, shared_key
                    )
                    print(f'[DEBUG] Sent - {encrypted_message=}')
                    client_socket.send(encrypted_message)
                except BrokenPipeError:
                    print(
                        "[INFO] Nie można wysłać wiadomości. Połączenie z serwerem zostało przerwane."
                    )
                    stop_client = True
                    break
                except OSError:
                    print("[INFO] Połączenie z serwerem zostało zamknięte.")
                    stop_client = True
                    break
                except KeyboardInterrupt:
                    message = 'EndSessionC'
                    encrypted_message = crypto_utils.get_encrypted_message(
                        aes_key, message, shared_key
                    )
                    print(f'[DEBUG] Sent - {encrypted_message=}')
                    client_socket.send(encrypted_message)
                    stop_client = True
                    break
    except ConnectionRefusedError:
        print("[BŁĄD] Nie udało się połączyć z serwerem.")
    except Exception as e:
        print(f"[BŁĄD] Wystąpił błąd: {e}")
    finally:
        print("[INFO] Klient zakończył działanie.")
        sys.exit(0)


if __name__ == "__main__":
    start_client()
