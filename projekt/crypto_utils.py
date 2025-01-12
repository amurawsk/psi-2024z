from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import HMAC, SHA256


def generate_hmac(message, secret_key):
    hmac = HMAC.new(secret_key.encode(), message, SHA256)
    return hmac.digest()


def verify_hmac(message, hmac_to_verify, secret_key):
    generated_hmac = HMAC.new(secret_key.encode(), message, SHA256)
    return generated_hmac.digest() == hmac_to_verify


def get_encrypted_message(aes_key, message, shared_key):
    cipher = AES.new(aes_key, AES.MODE_CBC)
    encrypted_message = cipher.encrypt(pad(message.encode(), AES.block_size))
    hmac = generate_hmac(encrypted_message, str(shared_key))
    return hmac + cipher.iv + encrypted_message


def get_decrypted_message(aes_key, encrypted_data, shared_key):
    hmac_len = SHA256.digest_size
    iv_len = AES.block_size
    hmac_received = encrypted_data[:hmac_len]
    iv = encrypted_data[hmac_len : hmac_len + iv_len]
    encrypted_message = encrypted_data[hmac_len + iv_len :]

    if not verify_hmac(encrypted_message, hmac_received, str(shared_key)):
        raise ValueError(
            "Weryfikacja HMAC nie powiodła się. Wiadomość została zmodyfikowana."
        )

    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_message), AES.block_size)

    return decrypted_data.decode("utf-8")
