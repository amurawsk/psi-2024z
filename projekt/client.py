import socket
import threading
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


def send_message_to_server(client_socket, aes_key, shared_key, message):
    encrypted_message = crypto_utils.get_encrypted_message(aes_key, message, shared_key)
    logging.debug(f"Sent - {encrypted_message=}")
    client_socket.send(encrypted_message)


def handle_message_from_server(aes_key, shared_key, encrypted_data):
    logging.debug(f"Received - {encrypted_data=}")
    decrypted_message = crypto_utils.get_decrypted_message(aes_key, encrypted_data, shared_key)
    decrypted_message_type, decrypted_message = decrypted_message[:11], decrypted_message[11:]
    if decrypted_message_type == 'EndSessionS':
        logging.info("Serwer wymusił zakończenie połączenia.")
        return True
    elif decrypted_message_type == 'MessageData':
        logging.debug(f"Od serwera: {decrypted_message=}")
    else:
        logging.error('Wrong message type')
    return False


def receive_messages(client_socket, aes_key, shared_key):
    global stop_client
    try:
        while not stop_client:
            encrypted_data = client_socket.recv(1024)
            if not encrypted_data or handle_message_from_server(aes_key, shared_key, encrypted_data):
                stop_client = True
                break
    except ConnectionResetError:
        logging.info("Serwer wymusił zakończenie połączenia.")
    except OSError:
        logging.info("Połączenie z serwerem zostało przerwane.")
    finally:
        stop_client = True
        logging.info("Połączenie zakończone.")


def start_client(server_host="127.0.0.1", server_port=12345):
    global stop_client
    while True:
        print("\nDostępne opcje:")
        print("1. Zainicjalizuj połączenie")
        print("2. Zakończ")
        option = input("Wybierz opcję: ")
        if option == "1":
            try:
                stop_client = False
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    client_socket.connect((server_host, server_port))
                    shared_key = establish_connection(client_socket)
                    aes_key = hashlib.sha256(str(shared_key).encode()).digest()

                    logging.info(f"Połączono z serwerem {server_host}:{server_port}")
                    logging.debug(f"Secrets - {shared_key=}, {aes_key=}")

                    threading.Thread(target=receive_messages, args=(client_socket, aes_key, shared_key,), daemon=True).start()

                    while not stop_client:
                        try:
                            print("\nDostępne opcje:")
                            print("1. Wyślij wiadomość")
                            print("2. Zakończ połączenie")
                            option = input("Wybierz opcję: ")
                            
                            if option == "1":
                                raw_message = input("Message: ")
                                if stop_client:
                                    break
                                send_message_to_server(client_socket, aes_key, shared_key, 'MessageData' + raw_message)
                            elif option == "2":
                                send_message_to_server(client_socket, aes_key, shared_key, 'EndSessionC')
                                stop_client = True
                                break
                            else:
                                print('Nieznana opcja!')
                        except KeyboardInterrupt:
                            send_message_to_server(client_socket, aes_key, shared_key, 'EndSessionC')
                            stop_client = True
                            break
                        except Exception:
                            logging.info("Nie można wysłać wiadomości. Połączenie z serwerem zostało przerwane.")
                            stop_client = True
                            break
            except Exception as e:
                logging.error(f"Wystąpił błąd: {e}")
                stop_client = True
            finally:
                logging.info("Klient zakończył działanie.")
        elif option == "2":
            break
        else:
            print('Nieznana opcja!')


if __name__ == "__main__":
    start_client()
