import os
from cryptography.fernet import Fernet
from utils.password_manager import derive_key

def encrypt_file(filepath: str, password: str, output_folder: str):
    with open(filepath, "rb") as f:
        data = f.read()

    # Gerar salt aleatório
    salt = os.urandom(16)
    key = derive_key(password, salt)
    cipher = Fernet(key)

    encrypted_data = cipher.encrypt(data)

    filename = os.path.basename(filepath)
    output_path = os.path.join(output_folder, filename + ".enc")

    # Salvar salt + dados criptografados
    with open(output_path, "wb") as f:
        f.write(salt + encrypted_data)

    print(f"Arquivo criptografado: {output_path}")

def decrypt_file(filepath: str, password: str, output_folder: str):
    with open(filepath, "rb") as f:
        content = f.read()

    salt, encrypted_data = content[:16], content[16:]
    key = derive_key(password, salt)
    cipher = Fernet(key)

    decrypted_data = cipher.decrypt(encrypted_data)

    filename = os.path.basename(filepath).replace(".enc", "")
    output_path = os.path.join(output_folder, filename)

    with open(output_path, "wb") as f:
        f.write(decrypted_data)

    print(f"Arquivo descriptografado: {output_path}")
