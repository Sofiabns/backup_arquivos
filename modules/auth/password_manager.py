"""
Módulo de gerenciamento de senhas
Parte 1: Entrada da senha do usuário
"""

import getpass
import hashlib
import re

class PasswordManager:
    """Classe para gerenciamento seguro de senhas"""
    
    def __init__(self):
        self.min_length = 8
    
    def get_password(self):
        """
        Obtém a senha do usuário com validação de segurança
        
        Returns:
            str: Senha validada do usuário
        """
        print("\n🔐 CONFIGURAÇÃO DE SENHA")
        print("-" * 30)
        
        while True:
            password = getpass.getpass("Digite sua senha para criptografia: ")
            
            if self._validate_password(password):
                # Confirma a senha
                confirm_password = getpass.getpass("Confirme sua senha: ")
                
                if password == confirm_password:
                    print("✓ Senha configurada com sucesso!")
                    return password
                else:
                    print("✗ As senhas não coincidem. Tente novamente.\n")
            else:
                print("✗ Senha não atende aos critérios de segurança.\n")
    
    def _validate_password(self, password):
        """
        Valida a força da senha
        
        Args:
            password (str): Senha a ser validada
            
        Returns:
            bool: True se a senha for válida
        """
        if len(password) < self.min_length:
            print(f"A senha deve ter pelo menos {self.min_length} caracteres.")
            return False
        
        # Verifica se contém pelo menos uma letra maiúscula
        if not re.search(r'[A-Z]', password):
            print("A senha deve conter pelo menos uma letra maiúscula.")
            return False
        
        # Verifica se contém pelo menos uma letra minúscula
        if not re.search(r'[a-z]', password):
            print("A senha deve conter pelo menos uma letra minúscula.")
            return False
        
        # Verifica se contém pelo menos um número
        if not re.search(r'\d', password):
            print("A senha deve conter pelo menos um número.")
            return False
        
        # Verifica se contém pelo menos um caractere especial
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            print("A senha deve conter pelo menos um caractere especial.")
            return False
        
        return True
    
    def hash_password(self, password):
        """
        Gera um hash SHA-256 da senha para uso como chave
        
        Args:
            password (str): Senha original
            
        Returns:
            bytes: Hash SHA-256 da senha
        """
        return hashlib.sha256(password.encode('utf-8')).digest()
    
    def derive_key(self, password, salt=None):
        """
        Deriva uma chave criptográfica da senha usando PBKDF2
        
        Args:
            password (str): Senha original
            salt (bytes): Salt para derivação (opcional)
            
        Returns:
            tuple: (chave, salt)
        """
        import os
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        
        if salt is None:
            salt = os.urandom(16)  # Gera salt aleatório de 16 bytes
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # 32 bytes = 256 bits para AES-256
            salt=salt,
            iterations=100000,  # Número de iterações para maior segurança
        )
        
        key = kdf.derive(password.encode('utf-8'))
        return key, salt