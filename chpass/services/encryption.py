import json
import base64
from random import random

import win32crypt
from Cryptodome.Cipher import AES


def get_master_key(chrome_user_folder: str) -> bytes:
    with open(f"{chrome_user_folder}\\Local State", "r", encoding='utf-8') as f:
        local_state = f.read()
        local_state = json.loads(local_state)
        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]  # removing DPAPI
        return win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]


def decrypt_password(buff: bytes, master_key: bytes) -> str:
    iv = buff[3:15]
    payload = buff[15:]
    cipher = AES.new(master_key, AES.MODE_GCM, iv)
    decrypted_pass = cipher.decrypt(payload)
    return decrypted_pass[:-16].decode()  # remove suffix bytes


def encrypt_password(password: str, master_key: bytes) -> bytes:
    iv = ''.join([chr(random.randint(0, 0xFF)) for i in range(16)])
    cipher = AES.new(master_key, AES.MODE_GCM, iv)
    return cipher.encrypt(password)
