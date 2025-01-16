from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import HMAC, SHA256
import base64
import logging

logging.basicConfig(level=logging.DEBUG, format="\n%(asctime)s - %(levelname)s - %(message)s")


def encode_base64(data):
    return base64.b64encode(data).decode('utf-8')


def generate_hmac(data, secret_key):
    hmac = HMAC.new(secret_key.encode(), data, SHA256)
    return hmac.digest()


def verify_hmac(data, hmac_to_verify, secret_key):
    try:
        hmac = HMAC.new(secret_key.encode(), data, SHA256)
        hmac.verify(hmac_to_verify)
        return True
    except ValueError:
        return False


def get_encrypted_message(aes_key, message, shared_key):
    cipher = AES.new(aes_key, AES.MODE_CBC)
    iv = cipher.iv
    encrypted_message = cipher.encrypt(pad(message.encode(), AES.block_size))
    logging.debug(f'{encode_base64(aes_key)=}')
    logging.debug(f'{encode_base64(iv)=}')
    logging.debug(f'{encode_base64(encrypted_message)=}')
    hmac = generate_hmac(iv + encrypted_message, str(shared_key))
    return hmac + iv + encrypted_message


def get_decrypted_message(aes_key, encrypted_data, shared_key):
    hmac_len = SHA256.digest_size
    iv_len = AES.block_size
    hmac_received = encrypted_data[:hmac_len]
    iv = encrypted_data[hmac_len:hmac_len + iv_len]
    encrypted_message = encrypted_data[hmac_len + iv_len:]
    logging.debug(f'{encode_base64(aes_key)=}')
    logging.debug(f'{encode_base64(iv)=}')
    logging.debug(f'{encode_base64(encrypted_message)=}')
    if not verify_hmac(iv + encrypted_message, hmac_received, str(shared_key)):
        raise ValueError("Weryfikacja HMAC nie powiodła się. Wiadomość została zmodyfikowana.")
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_message), AES.block_size)

    return decrypted_data.decode("utf-8")
