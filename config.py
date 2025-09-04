import os

# Pasta de origem
SOURCE_FOLDER = "arquivos_originais"

# Pasta onde os arquivos criptografados serão salvos
BACKUP_FOLDER = "backup"

# Tamanho da chave AES
KEY_SIZE = 32  

# Interações para derivar a chave
KDF_ITERATIONS = 100_000

# Garantir que as pastas existem
os.makedirs(SOURCE_FOLDER, exist_ok=True)
os.makedirs(BACKUP_FOLDER, exist_ok=True)
