import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


def decode_base64(data):
    return base64.b64decode(data)


def decode_hex(data):
    return bytes.fromhex(data)


def get_decrypted_message(aes_key, iv, encrypted_message):
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    
    decrypted_data = unpad(cipher.decrypt(encrypted_message), AES.block_size)
    return decrypted_data.decode("utf-8")


def main(aes_key_base64, iv_base64, encrypted_message_hex):
    aes_key = decode_base64(aes_key_base64)
    iv = decode_base64(iv_base64)
    encrypted_message = decode_hex(encrypted_message_hex)
    encrypted_message = encrypted_message[48:] # aby pominac hmac i iv
    decrypted_message = get_decrypted_message(aes_key, iv, encrypted_message)
    print(f"Odszyfrowana wiadomość: {decrypted_message}")


# ------------------------------- DANE --------------------------------------
# z logów
aes_key_base64 = "TslZn8ID0XajAVNsLgkaGbyFJ1myVb1oGIEKQsX+0Uo="
iv_base64 = "A7KNUqNRHjS1mTOxQO18Pw=="
# z wiresharka (data w hex)
encrypted_message_hex = "464597a6e1d2b5cbe9a2f946ecbc0660b25da199e8bc9e4f6764a2283f375ed503b28d52a3511e34b59933b140ed7c3f21f010a67387410fe30cb362ee0bd5e1852368e5abc6aa7fc53ec879d13b368550d4dd3213a6bc8d1b374c97abcf135e"
# ---------------------------------------------------------------------------


if __name__ == '__main__':
    main(aes_key_base64, iv_base64, encrypted_message_hex)
