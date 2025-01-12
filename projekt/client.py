import socket
import threading
import sys
import hashlib
import random
import logging

import crypto_utils

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

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
            logging.debug(f"Received - {encrypted_data=}")
            decrypted_message = crypto_utils.get_decrypted_message(
                aes_key, encrypted_data, shared_key
            )
            if decrypted_message == 'EndSessionS':
                    logging.info("Serwer wymusił zakończenie połączenia.")
                    stop_client = True
                    break
            print(f"Od serwera: {decrypted_message=}")
    except ConnectionResetError:
        logging.info("Serwer wymusił zakończenie połączenia.")
    except OSError:
        logging.info("Połączenie z serwerem zostało przerwane.")
    finally:
        stop_client = True
        logging.info("Połączenie zakończone.")


def start_client(server_host="127.0.0.1", server_port=12345):
    global stop_client
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((server_host, server_port))

            shared_key = establish_connection(client_socket)
            aes_key = hashlib.sha256(str(shared_key).encode()).digest()

            logging.info(f"Połączono z serwerem {server_host}:{server_port}")
            logging.debug(f"Secrets - {shared_key=}, {aes_key=}")

            threading.Thread(
                target=receive_messages, args=(client_socket, aes_key, shared_key,), daemon=True
            ).start()

            while not stop_client:
                try:
                    message = input("Message: ")
                    if stop_client:
                        break
                    encrypted_message = crypto_utils.get_encrypted_message(
                        aes_key, message, shared_key
                    )
                    logging.debug(f"Sent - {encrypted_message=}")
                    client_socket.send(encrypted_message)
                except BrokenPipeError:
                    logging.info(
                        "Nie można wysłać wiadomości. Połączenie z serwerem zostało przerwane."
                    )
                    stop_client = True
                    break
                except OSError:
                    logging.info("Połączenie z serwerem zostało zamknięte.")
                    stop_client = True
                    break
                except KeyboardInterrupt:
                    message = 'EndSessionC'
                    encrypted_message = crypto_utils.get_encrypted_message(
                        aes_key, message, shared_key
                    )
                    logging.debug(f"Sent - {encrypted_message=}")
                    client_socket.send(encrypted_message)
                    stop_client = True
                    break
    except ConnectionRefusedError:
        logging.error("Nie udało się połączyć z serwerem.")
    except Exception as e:
        logging.error(f"Wystąpił błąd: {e}")
    finally:
        logging.info("Klient zakończył działanie.")
        sys.exit(0)


if __name__ == "__main__":
    start_client()
