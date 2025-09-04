"""
Módulo de criptografia AES
Parte 3: Criptografia com AES dos arquivos
"""

import os
import struct
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'auth'))
from password_manager import PasswordManager

class AESHandler:
    """Classe para manipulação de criptografia AES"""
    
    def __init__(self, password):
        """
        Inicializa o handler AES com a senha fornecida
        
        Args:
            password (str): Senha do usuário
        """
        self.password_manager = PasswordManager()
        self.key, _ = self.password_manager.derive_key(password)
        self.algorithm = algorithms.AES(self.key)
    
    def encrypt(self, data):
        """
        Criptografa dados usando AES-256-CBC
        
        Args:
            data (bytes): Dados a serem criptografados
            
        Returns:
            bytes: Dados criptografados (IV + salt + tamanho_original + dados_criptografados)
        """
        try:
            # Gera IV aleatório
            iv = os.urandom(16)  # 16 bytes para AES
            
            # Cria cipher com modo CBC
            cipher = Cipher(self.algorithm, modes.CBC(iv))
            encryptor = cipher.encryptor()
            
            # Aplica padding PKCS7
            padder = padding.PKCS7(128).padder()  # 128 bits = 16 bytes
            padded_data = padder.update(data)
            padded_data += padder.finalize()
            
            # Criptografa os dados
            encrypted_data = encryptor.update(padded_data)
            encrypted_data += encryptor.finalize()
            
            # Combina IV + tamanho original + dados criptografados
            result = iv + struct.pack('<Q', len(data)) + encrypted_data
            
            return result
            
        except Exception as e:
            raise Exception(f"Erro durante criptografia: {e}")
    
    def decrypt(self, encrypted_data):
        """
        Descriptografa dados usando AES-256-CBC
        
        Args:
            encrypted_data (bytes): Dados criptografados
            
        Returns:
            bytes: Dados originais descriptografados
        """
        try:
            if len(encrypted_data) < 24:  # IV (16) + tamanho (8) mínimo
                raise ValueError("Dados criptografados muito pequenos")
            
            # Extrai IV (primeiros 16 bytes)
            iv = encrypted_data[:16]
            
            # Extrai tamanho original (próximos 8 bytes)
            original_size = struct.unpack('<Q', encrypted_data[16:24])[0]
            
            # Extrai dados criptografados (resto)
            ciphertext = encrypted_data[24:]
            
            # Cria cipher com modo CBC
            cipher = Cipher(self.algorithm, modes.CBC(iv))
            decryptor = cipher.decryptor()
            
            # Descriptografa
            padded_data = decryptor.update(ciphertext)
            padded_data += decryptor.finalize()
            
            # Remove padding PKCS7
            unpadder = padding.PKCS7(128).unpadder()
            data = unpadder.update(padded_data)
            data += unpadder.finalize()
            
            # Verifica se o tamanho está correto
            if len(data) != original_size:
                raise ValueError("Tamanho dos dados descriptografados não confere")
            
            return data
            
        except Exception as e:
            raise Exception(f"Erro durante descriptografia: {e}")
    
    def encrypt_file(self, input_path, output_path):
        """
        Criptografa um arquivo completo
        
        Args:
            input_path (str): Caminho do arquivo original
            output_path (str): Caminho do arquivo criptografado
        """
        try:
            with open(input_path, 'rb') as infile:
                data = infile.read()
            
            encrypted_data = self.encrypt(data)
            
            with open(output_path, 'wb') as outfile:
                outfile.write(encrypted_data)
                
        except Exception as e:
            raise Exception(f"Erro ao criptografar arquivo {input_path}: {e}")
    
    def decrypt_file(self, input_path, output_path):
        """
        Descriptografa um arquivo completo
        
        Args:
            input_path (str): Caminho do arquivo criptografado
            output_path (str): Caminho do arquivo descriptografado
        """
        try:
            with open(input_path, 'rb') as infile:
                encrypted_data = infile.read()
            
            decrypted_data = self.decrypt(encrypted_data)
            
            with open(output_path, 'wb') as outfile:
                outfile.write(decrypted_data)
                
        except Exception as e:
            raise Exception(f"Erro ao descriptografar arquivo {input_path}: {e}")
    
    def get_file_info(self, encrypted_file_path):
        """
        Obtém informações sobre um arquivo criptografado
        
        Args:
            encrypted_file_path (str): Caminho do arquivo criptografado
            
        Returns:
            dict: Informações do arquivo
        """
        try:
            with open(encrypted_file_path, 'rb') as f:
                # Lê apenas os primeiros 24 bytes para obter informações
                header = f.read(24)
                
            if len(header) < 24:
                return {"error": "Arquivo muito pequeno para ser válido"}
            
            iv = header[:16]
            original_size = struct.unpack('<Q', header[16:24])[0]
            
            file_size = os.path.getsize(encrypted_file_path)
            
            return {
                "original_size": original_size,
                "encrypted_size": file_size,
                "iv_preview": iv[:4].hex(),  # Mostra apenas os primeiros 4 bytes do IV
                "overhead": file_size - original_size
            }
            
        except Exception as e:
            return {"error": f"Erro ao ler informações: {e}"}