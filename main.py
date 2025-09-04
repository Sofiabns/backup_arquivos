#!/usr/bin/env python3
"""
Sistema de Criptografia de Arquivos com AES
Programa principal com interface melhorada
"""

import os
import sys
from pathlib import Path
import time

# Adiciona o diretório dos módulos ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from auth.password_manager import PasswordManager
from crypto.aes_handler import AESHandler
from file_ops.file_manager import FileManager
from utils.logger import setup_logger

class CryptoInterface:
    """Interface principal do sistema de criptografia"""
    
    def __init__(self):
        self.logger = setup_logger()
        self.password_manager = PasswordManager()
        self.file_manager = FileManager()
        self.current_password = None
        self.current_folder = None
        
    def clear_screen(self):
        """Limpa a tela do terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title="SISTEMA DE CRIPTOGRAFIA AES"):
        """Imprime cabeçalho estilizado"""
        self.clear_screen()
        print("╔" + "═" * 58 + "╗")
        print(f"║{title:^58}║")
        print("╚" + "═" * 58 + "╝")
        print()
    
    def print_menu_box(self, title, options, show_back=True):
        """Imprime menu em formato de caixa"""
        width = max(len(title), max(len(opt) for opt in options)) + 10
        
        print("┌" + "─" * width + "┐")
        print(f"│{title:^{width}}│")
        print("├" + "─" * width + "┤")
        
        for i, option in enumerate(options, 1):
            print(f"│ {i}. {option:<{width-5}}│")
        
        if show_back:
            print(f"│ 0. ← Voltar{'':<{width-10}}│")
        
        print("└" + "─" * width + "┘")
        print()
    
    def wait_for_enter(self, message="Pressione ENTER para continuar..."):
        """Pausa e aguarda ENTER"""
        print(f"\n💡 {message}")
        input()
    
    def show_status(self):
        """Mostra status atual do sistema"""
        print("📊 STATUS ATUAL:")
        print("├─" + "─" * 50)
        
        if self.current_password:
            print("│ 🔐 Senha: ✅ Configurada")
        else:
            print("│ 🔐 Senha: ❌ Não configurada")
        
        if self.current_folder:
            files = self.file_manager.scan_folder(self.current_folder, silent=True)
            encrypted_files = [f for f in files if f.endswith('.encrypted')]
            regular_files = [f for f in files if not f.endswith('.encrypted')]
            
            print(f"│ 📁 Pasta: {self.current_folder}")
            print(f"│ 📄 Arquivos normais: {len(regular_files)}")
            print(f"│ 🔒 Arquivos criptografados: {len(encrypted_files)}")
        else:
            print("│ 📁 Pasta: ❌ Não selecionada")
        
        print("└─" + "─" * 50)
        print()

    def main_menu(self):
        """Menu principal melhorado"""
        while True:
            self.print_header()
            self.show_status()
            
            options = [
                "🔐 Configurar/Alterar Senha",
                "📁 Selecionar Pasta de Trabalho",
                "🔒 Criptografar Arquivos",
                "🔓 Descriptografar Arquivos",
                "📊 Visualizar Arquivos da Pasta",
                "🧹 Gerenciar Backups",
                "❌ Sair do Programa"
            ]
            
            self.print_menu_box("MENU PRINCIPAL", options, show_back=False)
            
            try:
                choice = input("👉 Escolha uma opção: ").strip()
                
                if choice == '1':
                    self.configure_password()
                elif choice == '2':
                    self.select_folder()
                elif choice == '3':
                    self.encrypt_files_menu()
                elif choice == '4':
                    self.decrypt_files_menu()
                elif choice == '5':
                    self.view_files()
                elif choice == '6':
                    self.manage_backups()
                elif choice == '7':
                    if self.confirm_exit():
                        break
                else:
                    self.show_error("Opção inválida! Digite um número de 1 a 7.")
                    
            except KeyboardInterrupt:
                if self.confirm_exit():
                    break
    
    def configure_password(self):
        """Configuração de senha"""
        self.print_header("CONFIGURAÇÃO DE SENHA")
        
        if self.current_password:
            print("⚠️  Já existe uma senha configurada.")
            print("Deseja alterar a senha atual?")
            
            if not self.confirm_action("Alterar senha"):
                return
        
        try:
            self.current_password = self.password_manager.get_password()
            self.show_success("Senha configurada com sucesso! 🎉")
            self.logger.info("Senha configurada pelo usuário")
            
        except Exception as e:
            self.show_error(f"Erro ao configurar senha: {e}")
        
        self.wait_for_enter()
    
    def select_folder(self):
        """Menu de seleção de pasta melhorado"""
        while True:
            self.print_header("SELEÇÃO DE PASTA DE TRABALHO")
            
            if self.current_folder:
                print(f"📁 Pasta atual: {self.current_folder}")
                print()
            
            options = [
                "🏠 Usar pasta atual do programa",
                "📂 Navegar e selecionar pasta",
                "⌨️  Digitar caminho da pasta",
                "📋 Visualizar conteúdo da pasta atual"
            ]
            
            self.print_menu_box("OPÇÕES DE PASTA", options)
            
            choice = input("👉 Escolha uma opção: ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                self.current_folder = Path.cwd()
                self.show_success(f"Pasta definida: {self.current_folder}")
                self.wait_for_enter()
                break
            elif choice == '2':
                if self.browse_folders():
                    break
            elif choice == '3':
                if self.input_folder_path():
                    break
            elif choice == '4':
                self.preview_current_folder()
            else:
                self.show_error("Opção inválida!")
                time.sleep(1)
    
    def browse_folders(self):
        """Navegador de pastas interativo"""
        current_path = self.current_folder or Path.cwd()
        
        while True:
            self.print_header(f"NAVEGADOR - {current_path}")
            
            try:
                items = []
                # Adiciona pasta pai se não estiver na raiz
                if current_path.parent != current_path:
                    items.append(("📁 ..", current_path.parent, "pasta"))
                
                # Lista diretórios
                dirs = [item for item in current_path.iterdir() if item.is_dir()]
                dirs.sort()
                
                for directory in dirs[:10]:  # Limita a 10 para não poluir
                    items.append((f"📁 {directory.name}", directory, "pasta"))
                
                if not items:
                    print("📭 Nenhuma pasta encontrada.")
                    self.wait_for_enter()
                    return False
                
                # Mostra opções
                for i, (display, path, tipo) in enumerate(items, 1):
                    print(f"{i:2}. {display}")
                
                print()
                print("S. 🎯 Selecionar esta pasta")
                print("0. ← Voltar")
                print()
                
                choice = input("👉 Escolha: ").strip().upper()
                
                if choice == '0':
                    return False
                elif choice == 'S':
                    self.current_folder = current_path
                    self.show_success(f"Pasta selecionada: {current_path}")
                    self.wait_for_enter()
                    return True
                elif choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(items):
                        _, new_path, tipo = items[idx]
                        if tipo == "pasta":
                            current_path = new_path
                    else:
                        self.show_error("Número inválido!")
                        time.sleep(1)
                else:
                    self.show_error("Opção inválida!")
                    time.sleep(1)
                    
            except PermissionError:
                self.show_error("Sem permissão para acessar esta pasta!")
                time.sleep(2)
                return False
            except Exception as e:
                self.show_error(f"Erro ao navegar: {e}")
                time.sleep(2)
                return False
    
    def input_folder_path(self):
        """Entrada manual do caminho da pasta"""
        self.print_header("ENTRADA MANUAL DE PASTA")
        
        print("Digite o caminho completo da pasta:")
        print("Exemplo: C:\\Users\\SeuUsuario\\Documentos")
        print("         /home/usuario/documentos")
        print()
        
        path_input = input("📂 Caminho: ").strip()
        
        if not path_input:
            return False
        
        try:
            folder_path = Path(path_input)
            
            if folder_path.exists() and folder_path.is_dir():
                self.current_folder = folder_path
                self.show_success(f"Pasta definida: {folder_path}")
                self.wait_for_enter()
                return True
            else:
                self.show_error("Pasta não encontrada ou inválida!")
                self.wait_for_enter()
                return False
                
        except Exception as e:
            self.show_error(f"Erro no caminho: {e}")
            self.wait_for_enter()
            return False
    
    def preview_current_folder(self):
        """Visualiza conteúdo da pasta atual"""
        if not self.current_folder:
            self.show_error("Nenhuma pasta selecionada!")
            self.wait_for_enter()
            return
        
        self.print_header(f"CONTEÚDO - {self.current_folder}")
        
        files = self.file_manager.scan_folder(self.current_folder, silent=True)
        encrypted_files = [f for f in files if f.endswith('.encrypted')]
        regular_files = [f for f in files if not f.endswith('.encrypted')]
        
        print(f"📊 RESUMO:")
        print(f"├─ Arquivos normais: {len(regular_files)}")
        print(f"└─ Arquivos criptografados: {len(encrypted_files)}")
        print()
        
        if regular_files:
            print("📄 ARQUIVOS NORMAIS:")
            for i, file_path in enumerate(regular_files[:10], 1):
                file_info = self.file_manager.get_file_stats(file_path)
                print(f"{i:2}. {file_info['name']} ({file_info['size_formatted']})")
            
            if len(regular_files) > 10:
                print(f"    ... e mais {len(regular_files) - 10} arquivos")
            print()
        
        if encrypted_files:
            print("🔒 ARQUIVOS CRIPTOGRAFADOS:")
            for i, file_path in enumerate(encrypted_files[:10], 1):
                file_info = self.file_manager.get_file_stats(file_path)
                print(f"{i:2}. {file_info['name']} ({file_info['size_formatted']})")
            
            if len(encrypted_files) > 10:
                print(f"    ... e mais {len(encrypted_files) - 10} arquivos")
        
        self.wait_for_enter()
    
    def encrypt_files_menu(self):
        """Menu de criptografia"""
        if not self.validate_prerequisites():
            return
        
        self.print_header("CRIPTOGRAFIA DE ARQUIVOS")
        
        files = self.file_manager.scan_folder(self.current_folder, silent=True)
        regular_files = [f for f in files if not f.endswith('.encrypted')]
        
        if not regular_files:
            self.show_error("Nenhum arquivo para criptografar encontrado!")
            self.wait_for_enter()
            return
        
        print(f"🔍 Encontrados {len(regular_files)} arquivo(s) para criptografar:")
        print()
        
        for i, file_path in enumerate(regular_files[:10], 1):
            file_info = self.file_manager.get_file_stats(file_path)
            print(f"{i:2}. {file_info['name']} ({file_info['size_formatted']})")
        
        if len(regular_files) > 10:
            print(f"    ... e mais {len(regular_files) - 10} arquivos")
        
        print()
        
        if self.confirm_action(f"Criptografar {len(regular_files)} arquivo(s)"):
            self.perform_encryption(regular_files)
        
        self.wait_for_enter()
    
    def decrypt_files_menu(self):
        """Menu de descriptografia"""
        if not self.validate_prerequisites():
            return
        
        self.print_header("DESCRIPTOGRAFIA DE ARQUIVOS")
        
        files = self.file_manager.scan_folder(self.current_folder, silent=True)
        encrypted_files = [f for f in files if f.endswith('.encrypted')]
        
        if not encrypted_files:
            self.show_error("Nenhum arquivo criptografado encontrado!")
            self.wait_for_enter()
            return
        
        print(f"🔍 Encontrados {len(encrypted_files)} arquivo(s) criptografado(s):")
        print()
        
        for i, file_path in enumerate(encrypted_files[:10], 1):
            file_info = self.file_manager.get_file_stats(file_path)
            print(f"{i:2}. {file_info['name']} ({file_info['size_formatted']})")
        
        if len(encrypted_files) > 10:
            print(f"    ... e mais {len(encrypted_files) - 10} arquivos")
        
        print()
        
        if self.confirm_action(f"Descriptografar {len(encrypted_files)} arquivo(s)"):
            self.perform_decryption(encrypted_files)
        
        self.wait_for_enter()
    
    def perform_encryption(self, files_to_encrypt):
        """Executa processo de criptografia"""
        try:
            aes_handler = AESHandler(self.current_password)
            backup_folder = self.file_manager.create_backup_folder()
            
            print("\n🔄 Iniciando criptografia...")
            
            successful = 0
            failed = 0
            
            for i, file_path in enumerate(files_to_encrypt, 1):
                try:
                    print(f"[{i}/{len(files_to_encrypt)}] Processando: {Path(file_path).name}")
                    
                    with open(file_path, 'rb') as f:
                        file_data = f.read()
                    
                    encrypted_data = aes_handler.encrypt(file_data)
                    
                    backup_file_path = backup_folder / f"{Path(file_path).name}.encrypted"
                    with open(backup_file_path, 'wb') as f:
                        f.write(encrypted_data)
                    
                    successful += 1
                    print(f"    ✅ Salvo em: {backup_file_path}")
                    
                except Exception as e:
                    failed += 1
                    print(f"    ❌ Erro: {e}")
                    self.logger.error(f"Erro ao criptografar {file_path}: {e}")
            
            print("\n" + "="*50)
            print("🎉 CRIPTOGRAFIA CONCLUÍDA!")
            print(f"✅ Sucessos: {successful}")
            print(f"❌ Falhas: {failed}")
            print(f"📁 Pasta de backup: {backup_folder}")
            
            self.logger.info(f"Criptografia concluída: {successful} sucessos, {failed} falhas")
            
        except Exception as e:
            self.show_error(f"Erro durante criptografia: {e}")
    
    def perform_decryption(self, files_to_decrypt):
        """Executa processo de descriptografia"""
        try:
            aes_handler = AESHandler(self.current_password)
            decrypted_folder = self.file_manager.create_decrypted_folder()
            
            print("\n🔄 Iniciando descriptografia...")
            
            successful = 0
            failed = 0
            
            for i, file_path in enumerate(files_to_decrypt, 1):
                try:
                    print(f"[{i}/{len(files_to_decrypt)}] Processando: {Path(file_path).name}")
                    
                    with open(file_path, 'rb') as f:
                        encrypted_data = f.read()
                    
                    decrypted_data = aes_handler.decrypt(encrypted_data)
                    
                    original_name = Path(file_path).stem
                    decrypted_file_path = decrypted_folder / original_name
                    
                    with open(decrypted_file_path, 'wb') as f:
                        f.write(decrypted_data)
                    
                    successful += 1
                    print(f"    ✅ Restaurado: {decrypted_file_path}")
                    
                except Exception as e:
                    failed += 1
                    print(f"    ❌ Erro: {e}")
                    if "decrypt" in str(e).lower():
                        print(f"    💡 Verifique se a senha está correta!")
                    self.logger.error(f"Erro ao descriptografar {file_path}: {e}")
            
            print("\n" + "="*50)
            print("🎉 DESCRIPTOGRAFIA CONCLUÍDA!")
            print(f"✅ Sucessos: {successful}")
            print(f"❌ Falhas: {failed}")
            print(f"📁 Pasta de saída: {decrypted_folder}")
            
            self.logger.info(f"Descriptografia concluída: {successful} sucessos, {failed} falhas")
            
        except Exception as e:
            self.show_error(f"Erro durante descriptografia: {e}")
    
    def view_files(self):
        """Visualização detalhada de arquivos"""
        if not self.current_folder:
            self.show_error("Selecione uma pasta primeiro!")
            self.wait_for_enter()
            return
        
        self.preview_current_folder()
    
    def manage_backups(self):
        """Gerenciamento de backups"""
        self.print_header("GERENCIAMENTO DE BACKUPS")
        
        options = [
            "📊 Listar backups existentes",
            "🧹 Limpar backups antigos",
            "📁 Abrir pasta de backups"
        ]
        
        self.print_menu_box("OPÇÕES DE BACKUP", options)
        
        choice = input("👉 Escolha uma opção: ").strip()
        
        if choice == '0':
            return
        elif choice == '1':
            self.list_backups()
        elif choice == '2':
            self.clean_backups()
        elif choice == '3':
            self.open_backup_folder()
        else:
            self.show_error("Opção inválida!")
        
        self.wait_for_enter()
    
    def list_backups(self):
        """Lista backups disponíveis"""
        print("\n📋 Buscando backups...")
        
        backup_folders = []
        for item in Path.cwd().iterdir():
            if item.is_dir() and (item.name.startswith('encrypted_backup_') or 
                                 item.name.startswith('decrypted_files_')):
                backup_folders.append(item)
        
        if not backup_folders:
            print("📭 Nenhum backup encontrado.")
            return
        
        backup_folders.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        print(f"\n📁 Encontrados {len(backup_folders)} backup(s):")
        
        for i, folder in enumerate(backup_folders, 1):
            files_count = len(list(folder.iterdir()))
            size = sum(f.stat().st_size for f in folder.rglob('*') if f.is_file())
            size_str = self.file_manager._format_file_size(size)
            mod_time = time.strftime("%d/%m/%Y %H:%M", 
                                   time.localtime(folder.stat().st_mtime))
            
            backup_type = "🔒 Criptografado" if "encrypted" in folder.name else "🔓 Descriptografado"
            
            print(f"{i:2}. {backup_type}")
            print(f"    📁 {folder.name}")
            print(f"    📊 {files_count} arquivo(s), {size_str}")
            print(f"    🕐 {mod_time}")
            print()
    
    def clean_backups(self):
        """Limpa backups antigos"""
        if self.confirm_action("Limpar backups antigos (manter apenas os 5 mais recentes)"):
            try:
                self.file_manager.clean_old_backups(max_backups=5)
                self.show_success("Limpeza de backups concluída!")
            except Exception as e:
                self.show_error(f"Erro durante limpeza: {e}")
    
    def open_backup_folder(self):
        """Abre pasta de backups no explorador"""
        try:
            current_dir = Path.cwd()
            
            if os.name == 'nt':  # Windows
                os.startfile(current_dir)
            elif os.name == 'posix':  # Linux/Mac
                os.system(f'xdg-open "{current_dir}"' if 'linux' in sys.platform else f'open "{current_dir}"')
            
            self.show_success("Pasta aberta no explorador de arquivos!")
            
        except Exception as e:
            self.show_error(f"Erro ao abrir pasta: {e}")
    
    def validate_prerequisites(self):
        """Valida pré-requisitos para operações"""
        if not self.current_password:
            self.show_error("Configure uma senha primeiro!")
            self.wait_for_enter()
            return False
        
        if not self.current_folder:
            self.show_error("Selecione uma pasta de trabalho primeiro!")
            self.wait_for_enter()
            return False
        
        return True
    
    def confirm_action(self, action):
        """Confirmação de ação"""
        while True:
            response = input(f"❓ {action}? (S/n): ").strip().lower()
            if response in ['s', 'sim', 'y', 'yes', '']:
                return True
            elif response in ['n', 'nao', 'não', 'no']:
                return False
            else:
                print("Por favor, responda com 'S' para Sim ou 'N' para Não.")
    
    def confirm_exit(self):
        """Confirmação de saída"""
        return self.confirm_action("Deseja realmente sair do programa")
    
    def show_success(self, message):
        """Mostra mensagem de sucesso"""
        print(f"\n✅ {message}")
    
    def show_error(self, message):
        """Mostra mensagem de erro"""
        print(f"\n❌ {message}")
    
    def run(self):
        """Executa o programa principal"""
        try:
            self.logger.info("Sistema iniciado")
            self.main_menu()
            
        except KeyboardInterrupt:
            self.print_header()
            print("👋 Programa interrompido pelo usuário.")
            
        except Exception as e:
            self.logger.error(f"Erro crítico: {e}")
            print(f"\n💥 Erro crítico: {e}")
            
        finally:
            self.logger.info("Sistema encerrado")
            print("\n👋 Obrigado por usar o Sistema de Criptografia AES!")

def main():
    """Função principal"""
    app = CryptoInterface()
    app.run()

if __name__ == "__main__":
    main()