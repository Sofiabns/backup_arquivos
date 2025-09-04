import os
from config import SOURCE_FOLDER

def list_files():
    """Lista todos os arquivos da pasta de origem"""
    return [os.path.join(SOURCE_FOLDER, f) for f in os.listdir(SOURCE_FOLDER)]
