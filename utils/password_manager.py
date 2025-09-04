import getpass
import hashlib
import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from config import KEY_SIZE, KDF_ITERATIONS

def get_user_password():
    return getpass.getpass("Digite sua senha: ")

def derive_key(password: str, salt: bytes) -> bytes:
    """Deriva a chave AES a partir da senha e do salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=KDF_ITERATIONS,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))
