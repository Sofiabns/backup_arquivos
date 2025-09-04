"""
Módulo de gerenciamento de arquivos
Parte 2: Acesso à pasta original e leitura dos arquivos
Parte 4: Salvamento dos arquivos criptografados em outra pasta
"""

import os
from pathlib import Path
from datetime import datetime

class FileManager:
    """Classe para gerenciamento de arquivos e pastas"""
    
    def __init__(self):
        self.current_dir = Path.cwd()
        self.supported_extensions = {
            '.txt', '.doc', '.docx', '.pdf', '.jpg', '.jpeg', '.png', '.gif',
            '.mp4', '.avi', '.mp3', '.wav', '.zip', '.rar', '.xlsx', '.xls',
            '.pptx', '.ppt', '.py', '.js', '.html', '.css', '.json', '.xml',
            '.csv', '.encrypted'  # Incluindo arquivos já criptografados
        }
    
    def get_source_folder(self):
        """
        Obtém a pasta de origem dos arquivos a serem processados
        
        Returns:
            Path: Caminho da pasta de origem
        """
        print("\n📁 SELEÇÃO DE PASTA DE ORIGEM")
        print("-" * 35)
        print(f"Pasta atual: {self.current_dir}")
        
        while True:
            choice = input("\nEscolha uma opção:\n"
                          "1. Usar pasta atual\n"
                          "2. Especificar outra pasta\n"
                          "3. Listar subpastas da pasta atual\n"
                          "Digite sua escolha (1-3): ").strip()
            
            if choice == '1':
                return self.current_dir
            
            elif choice == '2':
                folder_path = input("Digite o caminho da pasta: ").strip()
                folder_path = Path(folder_path)
                
                if folder_path.exists() and folder_path.is_dir():
                    return folder_path
                else:
                    print("❌ Pasta não encontrada ou inválida!")
            
            elif choice == '3':
                self._list_subdirectories(self.current_dir)
            
            else:
                print("Opção inválida!")
    
    def scan_folder(self, folder_path, silent=False):
        """
        Escaneia uma pasta em busca de arquivos suportados
        
        Args:
            folder_path (Path): Caminho da pasta a ser escaneada
            silent (bool): Se True, não imprime saída
            
        Returns:
            list: Lista de caminhos dos arquivos encontrados
        """
        files_found = []
        
        try:
            for item in folder_path.iterdir():
                if item.is_file() and item.suffix.lower() in self.supported_extensions:
                    files_found.append(str(item))
            
            # Ordena os arquivos por nome
            files_found.sort()
            
            if not silent:
                print(f"\n📋 ARQUIVOS ENCONTRADOS")
                print("-" * 25)
                
                if files_found:
                    for i, file_path in enumerate(files_found, 1):
                        file_size = self._format_file_size(Path(file_path).stat().st_size)
                        print(f"{i:2d}. {Path(file_path).name} ({file_size})")
                else:
                    print("Nenhum arquivo suportado encontrado.")
                    print(f"Extensões suportadas: {', '.join(sorted(self.supported_extensions))}")
            
            return files_found
            
        except Exception as e:
            if not silent:
                print(f"Erro ao escanear pasta: {e}")
            return []
    
    def create_backup_folder(self):
        """
        Cria uma pasta de backup para arquivos criptografados
        
        Returns:
            Path: Caminho da pasta de backup criada
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_folder = self.current_dir / f"encrypted_backup_{timestamp}"
        
        try:
            backup_folder.mkdir(exist_ok=True)
            print(f"\n📂 Pasta de backup criada: {backup_folder}")
            return backup_folder
            
        except Exception as e:
            raise Exception(f"Erro ao criar pasta de backup: {e}")
    
    def create_decrypted_folder(self):
        """
        Cria uma pasta para arquivos descriptografados
        
        Returns:
            Path: Caminho da pasta de descriptografia criada
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        decrypted_folder = self.current_dir / f"decrypted_files_{timestamp}"
        
        try:
            decrypted_folder.mkdir(exist_ok=True)
            print(f"\n📂 Pasta de descriptografia criada: {decrypted_folder}")
            return decrypted_folder
            
        except Exception as e:
            raise Exception(f"Erro ao criar pasta de descriptografia: {e}")
    
    def _list_subdirectories(self, path):
        """Lista subdiretórios de uma pasta"""
        try:
            subdirs = [item for item in path.iterdir() if item.is_dir()]
            
            if subdirs:
                print(f"\n📁 Subpastas em {path}:")
                for i, subdir in enumerate(subdirs, 1):
                    print(f"{i:2d}. {subdir.name}")
            else:
                print(f"Nenhuma subpasta encontrada em {path}")
                
        except Exception as e:
            print(f"Erro ao listar subpastas: {e}")
    
    def _format_file_size(self, size_bytes):
        """
        Formata o tamanho do arquivo em uma string legível
        
        Args:
            size_bytes (int): Tamanho em bytes
            
        Returns:
            str: Tamanho formatado
        """
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
    
    def get_file_stats(self, file_path):
        """
        Obtém estatísticas detalhadas de um arquivo
        
        Args:
            file_path (str): Caminho do arquivo
            
        Returns:
            dict: Estatísticas do arquivo
        """
        try:
            path = Path(file_path)
            stat = path.stat()
            
            return {
                "name": path.name,
                "size": stat.st_size,
                "size_formatted": self._format_file_size(stat.st_size),
                "extension": path.suffix.lower(),
                "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                "created": datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            return {"error": f"Erro ao obter estatísticas: {e}"}
    
    def clean_old_backups(self, max_backups=5):
        """
        Remove backups antigos mantendo apenas os mais recentes
        
        Args:
            max_backups (int): Número máximo de backups a manter
        """
        try:
            backup_folders = []
            
            # Encontra todas as pastas de backup
            for item in self.current_dir.iterdir():
                if item.is_dir() and item.name.startswith('encrypted_backup_'):
                    backup_folders.append(item)
            
            # Ordena por data de modificação (mais recente primeiro)
            backup_folders.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            # Remove backups excedentes
            if len(backup_folders) > max_backups:
                for old_backup in backup_folders[max_backups:]:
                    print(f"Removendo backup antigo: {old_backup.name}")
                    import shutil
                    shutil.rmtree(old_backup)
                    
        except Exception as e:
            print(f"Aviso: Erro ao limpar backups antigos: {e}")