#!/usr/bin/env python3
"""
Sistema de Criptografia de Arquivos com AES
Programa principal que integra todos os módulos
"""

import os
import sys
from pathlib import Path

# Adiciona o diretório dos módulos ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from auth.password_manager import PasswordManager
from crypto.aes_handler import AESHandler
from file_ops.file_manager import FileManager
from utils.logger import setup_logger

def main():
    """Função principal do programa"""
    logger = setup_logger()
    logger.info("Iniciando sistema de criptografia de arquivos")
    
    print("=" * 50)
    print("  Sistema de Criptografia de Arquivos AES")
    print("=" * 50)
    
    try:
        # Parte 1: Entrada da senha do usuário
        password_manager = PasswordManager()
        password = password_manager.get_password()
        
        # Parte 2: Acesso à pasta original e leitura dos arquivos
        file_manager = FileManager()
        source_folder = file_manager.get_source_folder()
        files_to_process = file_manager.scan_folder(source_folder)
        
        if not files_to_process:
            print("Nenhum arquivo encontrado na pasta especificada.")
            return
        
        print(f"\nEncontrados {len(files_to_process)} arquivo(s) para processar:")
        for file_path in files_to_process:
            print(f"  - {file_path}")
        
        # Menu de operações
        while True:
            print("\n" + "=" * 30)
            print("Escolha uma operação:")
            print("1. Criptografar arquivos")
            print("2. Descriptografar arquivos")
            print("3. Sair")
            print("=" * 30)
            
            choice = input("Digite sua escolha (1-3): ").strip()
            
            if choice == '1':
                encrypt_files(password, files_to_process, file_manager, logger)
            elif choice == '2':
                decrypt_files(password, files_to_process, file_manager, logger)
            elif choice == '3':
                print("Encerrando programa...")
                break
            else:
                print("Opção inválida! Tente novamente.")
    
    except KeyboardInterrupt:
        print("\n\nPrograma interrompido pelo usuário.")
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        print(f"Erro inesperado: {e}")

def encrypt_files(password, files_to_process, file_manager, logger):
    """Parte 3 e 4: Criptografia AES e backup"""
    try:
        aes_handler = AESHandler(password)
        
        # Parte 4: Salvamento em pasta de backup
        backup_folder = file_manager.create_backup_folder()
        
        encrypted_count = 0
        for file_path in files_to_process:
            try:
                print(f"\nCriptografando: {file_path}")
                
                # Lê o arquivo original
                with open(file_path, 'rb') as f:
                    file_data = f.read()
                
                # Criptografa os dados
                encrypted_data = aes_handler.encrypt(file_data)
                
                # Salva o arquivo criptografado na pasta de backup
                backup_file_path = backup_folder / f"{Path(file_path).name}.encrypted"
                with open(backup_file_path, 'wb') as f:
                    f.write(encrypted_data)
                
                encrypted_count += 1
                logger.info(f"Arquivo criptografado: {file_path} -> {backup_file_path}")
                print(f"✓ Salvo como: {backup_file_path}")
                
            except Exception as e:
                logger.error(f"Erro ao criptografar {file_path}: {e}")
                print(f"✗ Erro ao criptografar {file_path}: {e}")
        
        print(f"\n🔒 Criptografia concluída!")
        print(f"Arquivos processados: {encrypted_count}/{len(files_to_process)}")
        print(f"Pasta de backup: {backup_folder}")
        
    except Exception as e:
        logger.error(f"Erro durante criptografia: {e}")
        print(f"Erro durante criptografia: {e}")

def decrypt_files(password, files_to_process, file_manager, logger):
    """Parte 5: Descriptografia dos arquivos"""
    try:
        aes_handler = AESHandler(password)
        
        # Filtra apenas arquivos .encrypted
        encrypted_files = [f for f in files_to_process if f.endswith('.encrypted')]
        
        if not encrypted_files:
            print("Nenhum arquivo criptografado (.encrypted) encontrado na pasta.")
            return
        
        # Pasta para arquivos descriptografados
        decrypted_folder = file_manager.create_decrypted_folder()
        
        decrypted_count = 0
        for file_path in encrypted_files:
            try:
                print(f"\nDescriptografando: {file_path}")
                
                # Lê o arquivo criptografado
                with open(file_path, 'rb') as f:
                    encrypted_data = f.read()
                
                # Descriptografa os dados
                decrypted_data = aes_handler.decrypt(encrypted_data)
                
                # Remove a extensão .encrypted do nome do arquivo
                original_name = Path(file_path).stem
                decrypted_file_path = decrypted_folder / original_name
                
                # Salva o arquivo descriptografado
                with open(decrypted_file_path, 'wb') as f:
                    f.write(decrypted_data)
                
                decrypted_count += 1
                logger.info(f"Arquivo descriptografado: {file_path} -> {decrypted_file_path}")
                print(f"✓ Salvo como: {decrypted_file_path}")
                
            except Exception as e:
                logger.error(f"Erro ao descriptografar {file_path}: {e}")
                print(f"✗ Erro ao descriptografar {file_path}: {e}")
                print("  (Verifique se a senha está correta)")
        
        print(f"\n🔓 Descriptografia concluída!")
        print(f"Arquivos processados: {decrypted_count}/{len(encrypted_files)}")
        print(f"Pasta de saída: {decrypted_folder}")
        
    except Exception as e:
        logger.error(f"Erro durante descriptografia: {e}")
        print(f"Erro durante descriptografia: {e}")

if __name__ == "__main__":
    main()