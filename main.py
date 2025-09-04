import os
from utils.password_manager import get_user_password
from utils.file_manager import list_files
from crypto.aes_cipher import encrypt_file, decrypt_file
from config import BACKUP_FOLDER, SOURCE_FOLDER

def main():
    print("=== Sistema de Criptografia AES ===")
    print("1 - Criptografar arquivos")
    print("2 - Descriptografar arquivos")
    choice = input("Escolha uma opção: ")

    password = get_user_password()

    if choice == "1":
        files = list_files()
        for f in files:
            encrypt_file(f, password, BACKUP_FOLDER)

    elif choice == "2":
        files = [os.path.join(BACKUP_FOLDER, f) for f in os.listdir(BACKUP_FOLDER) if f.endswith(".enc")]
        for f in files:
            decrypt_file(f, password, SOURCE_FOLDER)
    else:
        print("Opção inválida.")

if __name__ == "__main__":
    main()
